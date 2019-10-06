# COMP 151 Project 1

Mark Fraser

m_fraser3@u.pacific.edu

# Table of Contents

1. [COMP 151 Project 1](#comp-151-project-1)
2. [Table of Contents](#table-of-contents)
3. [Usage](#usage)
    1. [Args for next_move()](#args-for-next-move)
        1. [board](#board)
        2. [player](#player)
        3. [lookup_table](#lookup-table)
    2. [Global Variables](#global-variables)
        1. [search_depth](#search-depth)

# Usage

The program (identical between `PlayerX.py` and `PlayerO.py`) is integrated into the `Tournament.py` functionality.  The
`next_move()` function is the interface function to be run, and is run according
to the project instructions provided in the **Project 2 - Adversarial Search**
PDF.*  The **Args** section below is merely a reflection of the arguments
provided in `Tournament.py`.  The `load_player()` function is unimplemented in
favor of making the `next_move()` decision at runtime.

*NOTE: `next_move()` assumes that the input values are correct, as it has been
built to be run by `Tournament.py`.  If this function were to be made an
independent interface, argument validation would be necessary.

## Args for `next_move()`

### board

An instance of `C4Game`.  This is a representation of the Connect 4 game in its
current state.

### player

A character (either `X` or `O`), representing which character is supposed to
make the next move.

### lookup_table

In the case of this function, it does not matter what input this is, though when
run from `Tournament.py`, this will always be `None`, as the `load_player()`
function is not implemented and defaults to returning `None`.

## Global Variables

### search_depth

If you wish to test the algorithm with a different lookahead number, you can
change this to be any number `>= 1` for it to still be valid.  This global
variable is intended to be internal and always correct and is therefore not
supposed to be verified for an illegal value.
