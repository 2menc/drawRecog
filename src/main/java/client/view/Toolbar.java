package client.view;

import java.awt.Color;
import java.awt.event.ActionListener;
import java.util.List;

import javax.swing.*;

public class Toolbar extends JPanel{

    private final JButton eraser;
    private final JButton sender;
    private final JComboBox<String> modelChooseBox;

    public Toolbar() {
        this.eraser = new JButton("ERASE ALL");
        this.sender = new JButton("SEND");
        this.modelChooseBox = new JComboBox<>();

        this.eraser.setForeground(Color.RED);
        this.sender.setForeground(Color.GREEN);
        
        this.add(eraser);
        this.add(sender);
        this.add(this.modelChooseBox);
    }

    public void requestedToEraseAll(ActionListener al) {
        this.eraser.addActionListener(al);
    }

    public void requestedToSend(ActionListener al) {
        this.sender.addActionListener(al);
    }

    public void requestedToChangeModel(ActionListener al) {
        this.modelChooseBox.addActionListener(al);
    }

    public String getChosenModel() {
        return (String) this.modelChooseBox.getSelectedItem();
    }

    public void populateModelsCombo(List<String> modelNames) {
        for (var model: modelNames) {
            this.modelChooseBox.addItem(model);
        }
    }

}
