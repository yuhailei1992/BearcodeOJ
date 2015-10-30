public class Iterator {,,
    public static void main(String[] args) {
        int[] arr = {1, 2, 3, 4, 5};
        for (int i : arr) {
            for (int j : arr) {
                System.out.println(Integer.toString(i) + '\t' + Integer.toString(j));
            }
        }
        System.out.println((int)(0.5));
    }
}
