# py-git

Python based git to:

1. Learn git internals better

2. Learn python as additional language

## Commands Supported

1. init ✅

2. cat-file ✅

3. hash-object ✅

4. ls-tree ✅

5. write-tree ✅

6. commit-tree ✅

7. status ✅

8. commit ⌛️

9. diff 🕝

10. add - staging area 🕝

## Testing locally

The `your_program.sh` script is expected to operate on the `.git` folder inside
the current working directory. If you're running this inside the root of this
repository, you might end up accidentally damaging your repository's `.git`
folder.

We suggest executing `your_program.sh` in a different folder when testing
locally. For example:

```sh
mkdir -p /tmp/testing && cd /tmp/testing
/path/to/your/repo/your_program.sh init
```

▫️
To make this easier to type out, you could add a
[shell alias](https://shapeshed.com/unix-alias/):

```sh
alias pygit=/path/to/your/repo/your_program.sh

mkdir -p /tmp/testing && cd /tmp/testing
pygit init
```

### Credits

[codecrafters - git challenge](https://app.codecrafters.io/courses/git)

