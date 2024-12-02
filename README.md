# esolang ![](https://github.com/ains-arch/esolang/workflows/tests/badge.svg)

A simple esolang for experimenting with different syntax and semantics of programming languages.

To run the esolang, you can use the command `python3 -i esolang`, which will start the REPL interactively. You can also specify a specific level of the language to run by appending the `--level int` flag, where `int` is the level number you'd like to run.

For example:

```bash
python3 -i esolang --level 3
```

### 1. `if` Statements

An `if` statement follows the syntax:

```text
condition ? true_block : false_block
```

The condition is evaluated as `0` for `True` and non-zero for `False`. Based on the evaluation, either the `true_block` or the `false_block` will be executed.

#### Example 1: Basic `if` statement

```text
esolang> 1 ? 2 : 3
3
```

#### Example 2: Assigning values inside blocks with `if` statements and using comparison operators

```text
esolang> a = 0; { a == 0 } ? 2 : 3
2
esolang> a = 0; { a > 1 } ? 2 : 3
3
```

In this example, the value of `a` is checked. Because `a == 0`, the result is `2`. However, `a > 1`
is not true, so the result is `3`.

### 2. `for` Loops with Arbitrary Range

The `for` loop accepts a range, which can be computed using `range()` and iterates over each value within it.

#### Example 1: Basic `for` loop

```text
esolang> for i in range(10) {i}
9
```

The loop iterates over `range(10)` (which produces values from `0` to `9`) and the last value printed is `9`.

#### Example 2: Using `for` loop with variables

```text
esolang> a=0; for i in range(10) {a = a + i}
45
```

In this example, the `for` loop accumulates the sum of integers from `0` to `9`, and the value of `a` becomes `45`.

### 3. `while` Loops

A `while` loop runs as long as the condition evaluates to `True`. The loop will execute the `block` of code repeatedly.

#### Example 1: Basic `while` loop

```text
esolang> while 1 > 0 {1}
```

This loop will run indefinitely because the condition `1 > 0` is always true. The block `{1}` is executed. However, it doesn't print anything to the screen, because it never reaches a last value.

#### Example 2: Using a `while` loop with a counter

```text
esolang> a = 0; while a < 10 {a = a + 1}
10
```

In this example, the `while` loop increments the value of `a` until it reaches `10`.

### 4. Computing Prime Numbers with `for` and `while` Loops

To compute prime numbers, you can use a combination of a `for` loop and a `while` loop to check for divisibility.

#### Example: Prime number generator
```{text}
esolang> a = 2; while 0==0 { i = 2; is_prime = 0; while i < a { a % i ? {is_prime = 1} : {}; i = i + 1; }; is_prime ? print(a) : {}; a = a + 1; }
```

This script computes and prints prime numbers forever, as the outer `while` loop is always true. The inner `while` loop checks if a number is divisible by any number less than itself, and if it is not divisible, it prints the number (i.e., the prime number).

---

## Conclusion

This esolang supports basic control structures such as `if` statements, `for` loops, and `while` loops, as well as arithmetic operations. The syntax is inspired by C-style languages but simplified to allow easy block management and condition checking. The `for` loops in this language are flexible, accepting a range function, and the `while` loops provide powerful iteration capabilities for more complex tasks like prime number generation.
