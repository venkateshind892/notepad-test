import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.io.*;

public class Notepad extends JFrame {

    JTextArea textArea;

    public Notepad() {

        // Window
        setTitle("My Notepad");
        setSize(800, 600);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // Text Area
        textArea = new JTextArea();
        textArea.setFont(new Font("Arial", Font.PLAIN, 18));

        JScrollPane scrollPane = new JScrollPane(textArea);
        add(scrollPane);

        // Menu Bar
        JMenuBar menuBar = new JMenuBar();

        // File Menu
        JMenu fileMenu = new JMenu("File");

        JMenuItem newFile = new JMenuItem("New");
        JMenuItem openFile = new JMenuItem("Open");
        JMenuItem saveFile = new JMenuItem("Save");
        JMenuItem exit = new JMenuItem("Exit");

        // New
        newFile.addActionListener(e -> {
            textArea.setText("");
        });

        // Open
        openFile.addActionListener(e -> {
            JFileChooser fileChooser = new JFileChooser();

            int result = fileChooser.showOpenDialog(this);

            if (result == JFileChooser.APPROVE_OPTION) {

                File file = fileChooser.getSelectedFile();

                try {
                    BufferedReader reader =
                            new BufferedReader(new FileReader(file));

                    textArea.read(reader, null);
                    reader.close();

                } catch (IOException ex) {
                    JOptionPane.showMessageDialog(
                            this,
                            "Error opening file!"
                    );
                }
            }
        });

        // Save
        saveFile.addActionListener(e -> {

            JFileChooser fileChooser = new JFileChooser();

            int result = fileChooser.showSaveDialog(this);

            if (result == JFileChooser.APPROVE_OPTION) {

                File file = fileChooser.getSelectedFile();

                try {
                    BufferedWriter writer =
                            new BufferedWriter(new FileWriter(file));

                    textArea.write(writer);
                    writer.close();

                    JOptionPane.showMessageDialog(
                            this,
                            "File saved successfully!"
                    );

                } catch (IOException ex) {
                    JOptionPane.showMessageDialog(
                            this,
                            "Error saving file!"
                    );
                }
            }
        });

        // Exit
        exit.addActionListener(e -> {
            System.exit(0);
        });

        // Add items
        fileMenu.add(newFile);
        fileMenu.add(openFile);
        fileMenu.add(saveFile);
        fileMenu.addSeparator();
        fileMenu.add(exit);

        menuBar.add(fileMenu);

        setJMenuBar(menuBar);

        setLocationRelativeTo(null);
        setVisible(true);
    }

    public static void main(String[] args) {
        new Notepad();
    }
}
