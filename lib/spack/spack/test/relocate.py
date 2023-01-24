# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import io
import os
import os.path
import re
import shutil
import sys
from collections import OrderedDict

import pytest

import llnl.util.filesystem

import spack.concretize
import spack.paths
import spack.platforms
import spack.relocate
import spack.spec
import spack.store
import spack.tengine
import spack.util.executable
from spack.relocate import utf8_path_to_binary_regex, utf8_paths_to_single_binary_regex

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="Tests fail on Windows")


def skip_unless_linux(f):
    return pytest.mark.skipif(
        str(spack.platforms.real_host()) != "linux",
        reason="implementation currently requires linux",
    )(f)


def rpaths_for(new_binary):
    """Return the RPATHs or RUNPATHs of a binary."""
    patchelf = spack.util.executable.which("patchelf")
    output = patchelf("--print-rpath", str(new_binary), output=str)
    return output.strip()


def text_in_bin(text, binary):
    with open(str(binary), "rb") as f:
        data = f.read()
        f.seek(0)
        pat = re.compile(text.encode("utf-8"))
        if not pat.search(data):
            return False
        return True


@pytest.fixture(params=[True, False])
def is_relocatable(request):
    return request.param


@pytest.fixture()
def source_file(tmpdir, is_relocatable):
    """Returns the path to a source file of a relocatable executable."""
    if is_relocatable:
        template_src = os.path.join(spack.paths.test_path, "data", "templates", "relocatable.c")
        src = tmpdir.join("relocatable.c")
        shutil.copy(template_src, str(src))
    else:
        template_dirs = [os.path.join(spack.paths.test_path, "data", "templates")]
        env = spack.tengine.make_environment(template_dirs)
        template = env.get_template("non_relocatable.c")
        text = template.render({"prefix": spack.store.layout.root})

        src = tmpdir.join("non_relocatable.c")
        src.write(text)

    return src


@pytest.fixture()
def mock_patchelf(tmpdir, mock_executable):
    def _factory(output):
        return mock_executable("patchelf", output=output)

    return _factory


@pytest.fixture()
def make_dylib(tmpdir_factory):
    """Create a shared library with unfriendly qualities.

    - Writes the same rpath twice
    - Writes its install path as an absolute path
    """
    cc = spack.util.executable.which("cc")

    def _factory(abs_install_name="abs", extra_rpaths=[]):
        assert all(extra_rpaths)

        tmpdir = tmpdir_factory.mktemp(abs_install_name + "-".join(extra_rpaths).replace("/", ""))
        src = tmpdir.join("foo.c")
        src.write("int foo() { return 1; }\n")

        filename = "foo.dylib"
        lib = tmpdir.join(filename)

        args = ["-shared", str(src), "-o", str(lib)]
        rpaths = list(extra_rpaths)
        if abs_install_name.startswith("abs"):
            args += ["-install_name", str(lib)]
        else:
            args += ["-install_name", "@rpath/" + filename]

        if abs_install_name.endswith("rpath"):
            rpaths.append(str(tmpdir))

        args.extend("-Wl,-rpath," + s for s in rpaths)

        cc(*args)

        return (str(tmpdir), filename)

    return _factory


@pytest.fixture()
def make_object_file(tmpdir):
    cc = spack.util.executable.which("cc")

    def _factory():
        src = tmpdir.join("bar.c")
        src.write("int bar() { return 2; }\n")

        filename = "bar.o"
        lib = tmpdir.join(filename)

        args = ["-c", str(src), "-o", str(lib)]

        cc(*args)

        return (str(tmpdir), filename)

    return _factory


@pytest.fixture()
def copy_binary(prefix_like):
    """Returns a function that copies a binary somewhere and
    returns the new location.
    """

    def _copy_somewhere(orig_binary):
        new_root = orig_binary.mkdtemp().mkdir(prefix_like)
        new_binary = new_root.join("main.x")
        shutil.copy(str(orig_binary), str(new_binary))
        return new_binary

    return _copy_somewhere


@pytest.mark.requires_executables("/usr/bin/gcc", "patchelf", "strings", "file")
@skip_unless_linux
def test_ensure_binary_is_relocatable(source_file, is_relocatable):
    compiler = spack.util.executable.Executable("/usr/bin/gcc")
    executable = str(source_file).replace(".c", ".x")
    compiler_env = {"PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"}
    compiler(str(source_file), "-o", executable, env=compiler_env)

    assert spack.relocate.is_binary(executable)

    try:
        spack.relocate.ensure_binary_is_relocatable(executable)
        relocatable = True
    except spack.relocate.InstallRootStringError:
        relocatable = False

    assert relocatable == is_relocatable


@pytest.mark.requires_executables("patchelf", "strings", "file")
@skip_unless_linux
def test_patchelf_is_relocatable():
    patchelf = os.path.realpath(spack.relocate._patchelf())
    assert llnl.util.filesystem.is_exe(patchelf)
    spack.relocate.ensure_binary_is_relocatable(patchelf)


@skip_unless_linux
def test_ensure_binary_is_relocatable_errors(tmpdir):
    # The file passed in as argument must exist...
    with pytest.raises(ValueError) as exc_info:
        spack.relocate.ensure_binary_is_relocatable("/usr/bin/does_not_exist")
    assert "does not exist" in str(exc_info.value)

    # ...and the argument must be an absolute path to it
    file = tmpdir.join("delete.me")
    file.write("foo")

    with llnl.util.filesystem.working_dir(str(tmpdir)):
        with pytest.raises(ValueError) as exc_info:
            spack.relocate.ensure_binary_is_relocatable("delete.me")
        assert "is not an absolute path" in str(exc_info.value)


@pytest.mark.parametrize(
    "start_path,path_root,paths,expected",
    [
        (
            "/usr/bin/test",
            "/usr",
            ["/usr/lib", "/usr/lib64", "/opt/local/lib"],
            [
                os.path.join("$ORIGIN", "..", "lib"),
                os.path.join("$ORIGIN", "..", "lib64"),
                "/opt/local/lib",
            ],
        )
    ],
)
def test_make_relative_paths(start_path, path_root, paths, expected):
    relatives = spack.relocate._make_relative(start_path, path_root, paths)
    assert relatives == expected


@pytest.mark.parametrize(
    "start_path,relative_paths,expected",
    [
        # $ORIGIN will be replaced with os.path.dirname('usr/bin/test')
        # and then normalized
        (
            "/usr/bin/test",
            ["$ORIGIN/../lib", "$ORIGIN/../lib64", "/opt/local/lib"],
            [
                os.sep + os.path.join("usr", "lib"),
                os.sep + os.path.join("usr", "lib64"),
                "/opt/local/lib",
            ],
        ),
        # Relative path without $ORIGIN
        ("/usr/bin/test", ["../local/lib"], ["../local/lib"]),
    ],
)
def test_normalize_relative_paths(start_path, relative_paths, expected):
    normalized = spack.relocate._normalize_relative_paths(start_path, relative_paths)
    assert normalized == expected


def test_set_elf_rpaths(mock_patchelf):
    # Try to relocate a mock version of patchelf and check
    # the call made to patchelf itself
    patchelf = mock_patchelf("echo $@")
    rpaths = ["/usr/lib", "/usr/lib64", "/opt/local/lib"]
    output = spack.relocate._set_elf_rpaths(patchelf, rpaths)

    # Assert that the arguments of the call to patchelf are as expected
    assert "--force-rpath" in output
    assert "--set-rpath " + ":".join(rpaths) in output
    assert patchelf in output


@skip_unless_linux
def test_set_elf_rpaths_warning(mock_patchelf):
    # Mock a failing patchelf command and ensure it warns users
    patchelf = mock_patchelf("exit 1")
    rpaths = ["/usr/lib", "/usr/lib64", "/opt/local/lib"]
    # To avoid using capfd in order to check if the warning was triggered
    # here we just check that output is not set
    output = spack.relocate._set_elf_rpaths(patchelf, rpaths)
    assert output is None


@pytest.mark.requires_executables("patchelf", "strings", "file", "gcc")
@skip_unless_linux
def test_replace_prefix_bin(binary_with_rpaths, prefix_like):
    prefix = "/usr/" + prefix_like
    prefix_bytes = prefix.encode("utf-8")
    new_prefix = "/foo/" + prefix_like
    new_prefix_bytes = new_prefix.encode("utf-8")
    # Compile an "Hello world!" executable and set RPATHs
    executable = binary_with_rpaths(rpaths=[prefix + "/lib", prefix + "/lib64"])

    # Relocate the RPATHs
    spack.relocate._replace_prefix_bin(str(executable), {prefix_bytes: new_prefix_bytes})

    # Some compilers add rpaths so ensure changes included in final result
    assert "%s/lib:%s/lib64" % (new_prefix, new_prefix) in rpaths_for(executable)


@pytest.mark.requires_executables("patchelf", "strings", "file", "gcc")
@skip_unless_linux
def test_relocate_elf_binaries_absolute_paths(binary_with_rpaths, copy_binary, prefix_tmpdir):
    # Create an executable, set some RPATHs, copy it to another location
    orig_binary = binary_with_rpaths(rpaths=[str(prefix_tmpdir.mkdir("lib")), "/usr/lib64"])
    new_binary = copy_binary(orig_binary)

    spack.relocate.relocate_elf_binaries(
        binaries=[str(new_binary)],
        orig_root=str(orig_binary.dirpath()),
        new_root=None,  # Not needed when relocating absolute paths
        new_prefixes={str(orig_binary.dirpath()): "/foo"},
        rel=False,
        # Not needed when relocating absolute paths
        orig_prefix=None,
        new_prefix=None,
    )

    # Some compilers add rpaths so ensure changes included in final result
    assert "/foo/lib:/usr/lib64" in rpaths_for(new_binary)


@pytest.mark.requires_executables("patchelf", "strings", "file", "gcc")
@skip_unless_linux
def test_relocate_elf_binaries_relative_paths(binary_with_rpaths, copy_binary):
    # Create an executable, set some RPATHs, copy it to another location
    orig_binary = binary_with_rpaths(rpaths=["lib", "lib64", "/opt/local/lib"])
    new_binary = copy_binary(orig_binary)

    spack.relocate.relocate_elf_binaries(
        binaries=[str(new_binary)],
        orig_root=str(orig_binary.dirpath()),
        new_root=str(new_binary.dirpath()),
        new_prefixes={str(orig_binary.dirpath()): "/foo"},
        rel=True,
        orig_prefix=str(orig_binary.dirpath()),
        new_prefix=str(new_binary.dirpath()),
    )

    # Some compilers add rpaths so ensure changes included in final result
    assert "/foo/lib:/foo/lib64:/opt/local/lib" in rpaths_for(new_binary)


@pytest.mark.requires_executables("patchelf", "strings", "file", "gcc")
@skip_unless_linux
def test_make_elf_binaries_relative(binary_with_rpaths, copy_binary, prefix_tmpdir):
    orig_binary = binary_with_rpaths(
        rpaths=[
            str(prefix_tmpdir.mkdir("lib")),
            str(prefix_tmpdir.mkdir("lib64")),
            "/opt/local/lib",
        ]
    )
    new_binary = copy_binary(orig_binary)

    spack.relocate.make_elf_binaries_relative(
        [str(new_binary)], [str(orig_binary)], str(orig_binary.dirpath())
    )

    # Some compilers add rpaths so ensure changes included in final result
    assert "$ORIGIN/lib:$ORIGIN/lib64:/opt/local/lib" in rpaths_for(new_binary)


@pytest.mark.requires_executables("patchelf", "strings", "file", "gcc")
@skip_unless_linux
def test_relocate_text_bin(binary_with_rpaths, copy_binary, prefix_tmpdir):
    orig_binary = binary_with_rpaths(
        rpaths=[
            str(prefix_tmpdir.mkdir("lib")),
            str(prefix_tmpdir.mkdir("lib64")),
            "/opt/local/lib",
        ],
        message=str(prefix_tmpdir),
    )
    new_binary = copy_binary(orig_binary)

    # Check original directory is in the executable and the new one is not
    assert text_in_bin(str(prefix_tmpdir), new_binary)
    assert not text_in_bin(str(new_binary.dirpath()), new_binary)

    # Check this call succeed
    orig_path_bytes = str(orig_binary.dirpath()).encode("utf-8")
    new_path_bytes = str(new_binary.dirpath()).encode("utf-8")

    spack.relocate.unsafe_relocate_text_bin([str(new_binary)], {orig_path_bytes: new_path_bytes})

    # Check original directory is not there anymore and it was
    # substituted with the new one
    assert not text_in_bin(str(prefix_tmpdir), new_binary)
    assert text_in_bin(str(new_binary.dirpath()), new_binary)


def test_relocate_text_bin_raise_if_new_prefix_is_longer(tmpdir):
    short_prefix = b"/short"
    long_prefix = b"/much/longer"
    fpath = str(tmpdir.join("fakebin"))
    with open(fpath, "w") as f:
        f.write("/short")
    with pytest.raises(spack.relocate.BinaryTextReplaceError):
        spack.relocate.unsafe_relocate_text_bin([fpath], {short_prefix: long_prefix})


@pytest.mark.requires_executables("install_name_tool", "file", "cc")
def test_fixup_macos_rpaths(make_dylib, make_object_file):
    # For each of these tests except for the "correct" case, the first fixup
    # should make changes, and the second fixup should be a null-op.
    fixup_rpath = spack.relocate.fixup_macos_rpath

    no_rpath = []
    duplicate_rpaths = ["/usr", "/usr"]
    bad_rpath = ["/nonexistent/path"]

    # Non-relocatable library id and duplicate rpaths
    (root, filename) = make_dylib("abs", duplicate_rpaths)
    assert fixup_rpath(root, filename)
    assert not fixup_rpath(root, filename)

    # Hardcoded but relocatable library id (but we do NOT relocate)
    (root, filename) = make_dylib("abs_with_rpath", no_rpath)
    assert not fixup_rpath(root, filename)

    # Library id uses rpath but there are extra duplicate rpaths
    (root, filename) = make_dylib("rpath", duplicate_rpaths)
    assert fixup_rpath(root, filename)
    assert not fixup_rpath(root, filename)

    # Shared library was constructed with relocatable id from the get-go
    (root, filename) = make_dylib("rpath", no_rpath)
    assert not fixup_rpath(root, filename)

    # Non-relocatable library id
    (root, filename) = make_dylib("abs", no_rpath)
    assert not fixup_rpath(root, filename)

    # Relocatable with executable paths and loader paths
    (root, filename) = make_dylib("rpath", ["@executable_path/../lib", "@loader_path"])
    assert not fixup_rpath(root, filename)

    # Non-relocatable library id but nonexistent rpath
    (root, filename) = make_dylib("abs", bad_rpath)
    assert fixup_rpath(root, filename)
    assert not fixup_rpath(root, filename)

    # Duplicate nonexistent rpath will need *two* passes
    (root, filename) = make_dylib("rpath", bad_rpath * 2)
    assert fixup_rpath(root, filename)
    assert fixup_rpath(root, filename)
    assert not fixup_rpath(root, filename)

    # Test on an object file, which *also* has type 'application/x-mach-binary'
    # but should be ignored (no ID headers, no RPATH)
    # (this is a corner case for GCC installation)
    (root, filename) = make_object_file()
    assert not fixup_rpath(root, filename)


def test_text_relocation_regex_is_safe():
    # Test whether prefix regex is properly escaped
    string = b"This does not match /a/, but this does: /[a-z]/."
    assert utf8_path_to_binary_regex("/[a-z]/").search(string).group(0) == b"/[a-z]/"


def test_utf8_paths_to_single_binary_regex():
    regex = utf8_paths_to_single_binary_regex(["/first/path", "/second/path", "/safe/[a-z]"])
    # Match nothing
    assert not regex.search(b"text /neither/first/path text /the/second/path text")

    # Match first
    string = b"contains both /first/path/subdir and /second/path/sub"
    assert regex.search(string).group(0) == b"/first/path/subdir"

    # Match second
    string = b"contains both /not/first/path/subdir but /second/path/subdir"
    assert regex.search(string).group(0) == b"/second/path/subdir"

    # Match "unsafe" dir name
    string = b"don't match /safe/a/path but do match /safe/[a-z]/file"
    assert regex.search(string).group(0) == b"/safe/[a-z]/file"


def test_ordered_replacement():
    # This tests whether binary text replacement respects order, so that
    # a long package prefix is replaced before a shorter sub-prefix like
    # the root of the spack store (as a fallback).
    def replace_and_expect(prefix_map, before, after=None, suffix_safety_size=7):
        f = io.BytesIO(before)
        spack.relocate.apply_binary_replacements(f, OrderedDict(prefix_map), suffix_safety_size)
        f.seek(0)
        assert f.read() == after

    # The case of having a non-null terminated common suffix.
    replace_and_expect(
        [
            (b"/old-spack/opt/specific-package", b"/first/specific-package"),
            (b"/old-spack/opt", b"/sec/spack/opt"),
        ],
        b"Binary with /old-spack/opt/specific-package and /old-spack/opt",
        b"Binary with /////////first/specific-package and /sec/spack/opt",
        suffix_safety_size=7,
    )

    # The case of having a direct null terminated common suffix.
    replace_and_expect(
        [
            (b"/old-spack/opt/specific-package", b"/first/specific-package"),
            (b"/old-spack/opt", b"/sec/spack/opt"),
        ],
        b"Binary with /old-spack/opt/specific-package\0 and /old-spack/opt\0",
        b"Binary with /////////first/specific-package\0 and /sec/spack/opt\0",
        suffix_safety_size=7,
    )

    # Testing the order of operations (not null terminated, long enough common suffix)
    replace_and_expect(
        [
            (b"/old-spack/opt", b"/s/spack/opt"),
            (b"/old-spack/opt/specific-package", b"/first/specific-package"),
        ],
        b"Binary with /old-spack/opt/specific-package and /old-spack/opt",
        b"Binary with ///s/spack/opt/specific-package and ///s/spack/opt",
        suffix_safety_size=7,
    )

    # Testing the order of operations (null terminated, long enough common suffix)
    replace_and_expect(
        [
            (b"/old-spack/opt", b"/s/spack/opt"),
            (b"/old-spack/opt/specific-package", b"/first/specific-package"),
        ],
        b"Binary with /old-spack/opt/specific-package\0 and /old-spack/opt\0",
        b"Binary with ///s/spack/opt/specific-package\0 and ///s/spack/opt\0",
        suffix_safety_size=7,
    )

    # Null terminated within the lookahead window, common suffix long enough
    replace_and_expect(
        [(b"/old-spack/opt/specific-package", b"/opt/specific-XXXXage")],
        b"Binary with /old-spack/opt/specific-package/sub\0 data",
        b"Binary with ///////////opt/specific-XXXXage/sub\0 data",
        suffix_safety_size=7,
    )

    # Null terminated within the lookahead window, common suffix too short, but
    # shortening is enough to spare more than 7 bytes of old suffix.
    replace_and_expect(
        [(b"/old-spack/opt/specific-package", b"/opt/specific-XXXXXge")],
        b"Binary with /old-spack/opt/specific-package/sub\0 data",
        b"Binary with /opt/specific-XXXXXge/sub\0ckage/sub\0 data",  # ckage/sub = 9 bytes
        suffix_safety_size=7,
    )

    # Null terminated within the lookahead window, common suffix too short,
    # shortening leaves exactly 7 suffix bytes untouched, amazing!
    replace_and_expect(
        [(b"/old-spack/opt/specific-package", b"/spack/specific-XXXXXge")],
        b"Binary with /old-spack/opt/specific-package/sub\0 data",
        b"Binary with /spack/specific-XXXXXge/sub\0age/sub\0 data",  # age/sub = 7 bytes
        suffix_safety_size=7,
    )

    # Null terminated within the lookahead window, common suffix too short,
    # shortening doesn't leave space for 7 bytes, sad!
    error_msg = "Cannot replace {!r} with {!r} in the C-string {!r}.".format(
        b"/old-spack/opt/specific-package",
        b"/snacks/specific-XXXXXge",
        b"/old-spack/opt/specific-package/sub",
    )
    with pytest.raises(spack.relocate.CannotShrinkCString, match=error_msg):
        replace_and_expect(
            [(b"/old-spack/opt/specific-package", b"/snacks/specific-XXXXXge")],
            b"Binary with /old-spack/opt/specific-package/sub\0 data",
            # expect failure!
            suffix_safety_size=7,
        )

    # Check that it works when changing suffix_safety_size.
    replace_and_expect(
        [(b"/old-spack/opt/specific-package", b"/snacks/specific-XXXXXXe")],
        b"Binary with /old-spack/opt/specific-package/sub\0 data",
        b"Binary with /snacks/specific-XXXXXXe/sub\0ge/sub\0 data",
        suffix_safety_size=6,
    )

    # Finally check the case of no shortening but a long enough common suffix.
    replace_and_expect(
        [(b"pkg-gwixwaalgczp6", b"pkg-zkesfralgczp6")],
        b"Binary with pkg-gwixwaalgczp6/config\0 data",
        b"Binary with pkg-zkesfralgczp6/config\0 data",
        suffix_safety_size=7,
    )

    # Too short matching suffix, identical string length
    error_msg = "Cannot replace {!r} with {!r} in the C-string {!r}.".format(
        b"pkg-gwixwaxlgczp6",
        b"pkg-zkesfrzlgczp6",
        b"pkg-gwixwaxlgczp6",
    )
    with pytest.raises(spack.relocate.CannotShrinkCString, match=error_msg):
        replace_and_expect(
            [(b"pkg-gwixwaxlgczp6", b"pkg-zkesfrzlgczp6")],
            b"Binary with pkg-gwixwaxlgczp6\0 data",
            # expect failure
            suffix_safety_size=7,
        )

    # Finally, make sure that the regex is not greedily finding the LAST null byte
    # it should find the first null byte in the window. In this test we put one null
    # at a distance where we cant keep a long enough suffix, and one where we can,
    # so we should expect failure when the first null is used.
    error_msg = "Cannot replace {!r} with {!r} in the C-string {!r}.".format(
        b"pkg-abcdef",
        b"pkg-xyzabc",
        b"pkg-abcdef",
    )
    with pytest.raises(spack.relocate.CannotShrinkCString, match=error_msg):
        replace_and_expect(
            [(b"pkg-abcdef", b"pkg-xyzabc")],
            b"Binary with pkg-abcdef\0/xx\0",  # def\0/xx is 7 bytes.
            # expect failure
            suffix_safety_size=7,
        )


def test_inplace_text_replacement():
    def replace_and_expect(prefix_to_prefix, before: bytes, after: bytes):
        f = io.BytesIO(before)
        prefix_to_prefix = OrderedDict(prefix_to_prefix)
        regex = spack.relocate.byte_strings_to_single_binary_regex(prefix_to_prefix.keys())
        spack.relocate._replace_prefix_text_file(f, regex, prefix_to_prefix)
        f.seek(0)
        assert f.read() == after

    replace_and_expect(
        [
            (b"/first/prefix", b"/first-replacement/prefix"),
            (b"/second/prefix", b"/second-replacement/prefix"),
        ],
        b"Example: /first/prefix/subdir and /second/prefix/subdir",
        b"Example: /first-replacement/prefix/subdir and /second-replacement/prefix/subdir",
    )

    replace_and_expect(
        [
            (b"/replace/in/order", b"/first"),
            (b"/replace/in", b"/second"),
            (b"/replace", b"/third"),
        ],
        b"/replace/in/order/x /replace/in/y /replace/z",
        b"/first/x /second/y /third/z",
    )

    replace_and_expect(
        [
            (b"/replace", b"/third"),
            (b"/replace/in", b"/second"),
            (b"/replace/in/order", b"/first"),
        ],
        b"/replace/in/order/x /replace/in/y /replace/z",
        b"/third/in/order/x /third/in/y /third/z",
    )

    replace_and_expect(
        [(b"/my/prefix", b"/replacement")],
        b"/dont/replace/my/prefix #!/dont/replace/my/prefix",
        b"/dont/replace/my/prefix #!/dont/replace/my/prefix",
    )

    replace_and_expect(
        [(b"/my/prefix", b"/replacement")],
        b"Install path: /my/prefix.",
        b"Install path: /replacement.",
    )

    replace_and_expect(
        [(b"/my/prefix", b"/replacement")],
        b"#!/my/prefix",
        b"#!/replacement",
    )
