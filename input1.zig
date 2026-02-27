const x: int = 10;
var y: int = 5;

fn add(a: int, b: int) int {
    var c: int = a + b;
    return c;
}

fn main() int {
    if (x > y) {
        y = x;
    } else {
        y = y + 1;
    }

    var x: int = add(10, 50);
    return x;
}