
package p2333;
public class Solution {
    public static void main(String[] args) {
        int ret = 1; // Assume wrong answer.
        if (1 == foo(1) && 2 == foo(2)) {
            ret = 100;
        }
        System.exit(ret);
    }

    
    public static int foo(int x) {
        return x;
    }

}
