package cn.sealiu;
import java.util.Calendar;

public class Main {

    public static void main(String[] args) {
        // write your code here
        Calendar calendar = Calendar.getInstance();
        long now = calendar.getTimeInMillis();

        calendar.set(Calendar.DAY_OF_YEAR, 1);
        long star = calendar.getTimeInMillis();

        calendar.add(Calendar.YEAR, 1);
        long end = calendar.getTimeInMillis();

        float progress = Math.round(1000 * (now - star) / (end - star)) / 10f;

        String text = "";
        for (int i = 5; i <= 100; i += 5) {
            text += i <= progress ? '▓' : '░';
        }

        System.out.println();
        System.out.println("progress:" + text + " " + progress + "%");
    }
}
