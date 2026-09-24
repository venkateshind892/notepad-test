package com.example.notepad;

import android.app.AlertDialog;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.ArrayAdapter;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {

    EditText noteTitle;
    EditText noteContent;
    Button saveButton;
    Button newButton;
    Button deleteButton;
    ListView noteList;

    ArrayList<String> notes;
    ArrayAdapter<String> adapter;

    String selectedNote = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        noteTitle = findViewById(R.id.noteTitle);
        noteContent = findViewById(R.id.noteContent);
        saveButton = findViewById(R.id.saveButton);
        newButton = findViewById(R.id.newButton);
        deleteButton = findViewById(R.id.deleteButton);
        noteList = findViewById(R.id.noteList);

        notes = new ArrayList<>();

        loadNotes();

        adapter = new ArrayAdapter<>(
                this,
                android.R.layout.simple_list_item_1,
                notes
        );

        noteList.setAdapter(adapter);

        // NEW NOTE
        newButton.setOnClickListener(v -> {

            selectedNote = null;

            noteTitle.setText("");
            noteContent.setText("");

            Toast.makeText(
                    this,
                    "New note",
                    Toast.LENGTH_SHORT
            ).show();
        });

        // SAVE NOTE
        saveButton.setOnClickListener(v -> saveNote());

        // DELETE NOTE
        deleteButton.setOnClickListener(v -> deleteNote());

        // OPEN NOTE
        noteList.setOnItemClickListener(
                (parent, view, position, id) -> {

                    selectedNote = notes.get(position);

                    loadSelectedNote(selectedNote);
                }
        );
    }

    private void saveNote() {

        String title = noteTitle.getText().toString().trim();
        String content = noteContent.getText().toString();

        if (title.isEmpty()) {

            Toast.makeText(
                    this,
                    "Enter a note title",
                    Toast.LENGTH_SHORT
            ).show();

            return;
        }

        try {

            File file = new File(
                    getFilesDir(),
                    title + ".txt"
            );

            FileOutputStream output =
                    new FileOutputStream(file);

            output.write(content.getBytes());

            output.close();

            if (!notes.contains(title)) {
                notes.add(title);
            }

            adapter.notifyDataSetChanged();

            selectedNote = title;

            Toast.makeText(
                    this,
                    "Note saved",
                    Toast.LENGTH_SHORT
            ).show();

        } catch (Exception e) {

            Toast.makeText(
                    this,
                    "Save failed: " + e.getMessage(),
                    Toast.LENGTH_LONG
            ).show();
        }
    }

    private void loadNotes() {

        File directory = getFilesDir();

        File[] files = directory.listFiles();

        if (files == null) {
            return;
        }

        for (File file : files) {

            String name = file.getName();

            if (name.endsWith(".txt")) {

                String title =
                        name.substring(
                                0,
                                name.length() - 4
                        );

                notes.add(title);
            }
        }
    }

    private void loadSelectedNote(String title) {

        try {

            File file = new File(
                    getFilesDir(),
                    title + ".txt"
            );

            FileInputStream input =
                    new FileInputStream(file);

            byte[] data =
                    new byte[(int) file.length()];

            input.read(data);

            input.close();

            String content =
                    new String(data);

            noteTitle.setText(title);
            noteContent.setText(content);

        } catch (Exception e) {

            Toast.makeText(
                    this,
                    "Unable to open note",
                    Toast.LENGTH_SHORT
            ).show();
        }
    }

    private void deleteNote() {

        if (selectedNote == null) {

            Toast.makeText(
                    this,
                    "Select a note first",
                    Toast.LENGTH_SHORT
            ).show();

            return;
        }

        new AlertDialog.Builder(this)
                .setTitle("Delete Note")
                .setMessage(
                        "Are you sure you want to delete this note?"
                )
                .setPositiveButton(
                        "Delete",
                        (dialog, which) -> {

                            File file = new File(
                                    getFilesDir(),
                                    selectedNote + ".txt"
                            );

                            if (file.exists()) {
                                file.delete();
                            }

                            notes.remove(selectedNote);

                            adapter.notifyDataSetChanged();

                            noteTitle.setText("");
                            noteContent.setText("");

                            selectedNote = null;

                            Toast.makeText(
                                    this,
                                    "Note deleted",
                                    Toast.LENGTH_SHORT
                            ).show();
                        }
                )
                .setNegativeButton(
                        "Cancel",
                        null
                )
                .show();
    }
}
