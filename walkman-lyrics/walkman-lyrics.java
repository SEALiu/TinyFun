import java.io.*;
import java.util.Scanner;
import java.util.regex.*;

/**
 * Created by liuyang
 * on 2018/7/15.s
 */
public class Regex {

    private static void processLyric(String path, File lrcx) {
        String lrc_name = lrcx.getName().replaceAll("(.+) - (.+).lrcx", "$2 - $1.lrc");

        File file_path = new File(path + "/lrc/");
        if (!file_path.exists()) file_path.mkdirs();

        File lrc = new File(path + "/lrc/" + lrc_name);

        if (!lrc.exists()) {
            try {
                if (!lrc.createNewFile()) {
                   System.out.println ("Error! failed create file (" + lrc.getPath() + ")");
                    return;
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        Pattern regex = Pattern.compile("(?im)(^\\[(\\d{2}:\\d{2}.\\d{3})\\])(\\[t{2}\\]).+");
        Pattern regex_lrc = Pattern.compile("(?im)^\\[\\d{2}:\\d{2}.\\d{3}\\].*");

        try {
            FileOutputStream outStream = new FileOutputStream(lrc);

            BufferedReader reader = new BufferedReader(new FileReader(lrcx));
            String line;
            while ((line = reader.readLine()) != null) {
                Matcher m = regex.matcher(line);
                Matcher m_lrc = regex_lrc.matcher(line);

                if (m.find()) {
                    line = "";
                } else if (m_lrc.find()) {
                    line = line.replaceAll("\\[(\\d{2}):(\\d{2})\\.((\\d{2})\\d{1})\\]", "[$1:$2.$4]");
                    line += "\n";
                } else {
                    line += "\n";
                }

                if (!line.equals("")) {
                    byte[] line_bytes = line.getBytes();
                    outStream.write(line_bytes);
                }
            }

            outStream.close();
            reader.close();
            System.out.println(lrc.getName() + " completed!");

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {

        System.out.print("输入LyricsX歌词目录：");
        Scanner sc = new Scanner(System.in);
        String path = sc.nextLine();

        File file = new File(path);
        File[] array = file.listFiles();

        if (array == null) return;

        for (File f : array) {
            if (f.isFile() && f.getName().endsWith(".lrcx")) {
                processLyric(path, f);
            }
        }
    }
}
