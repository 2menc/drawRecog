package client.view;

import java.awt.Color;
import java.awt.event.ActionListener;

import javax.swing.*;

public class Toolbar extends JPanel{

    private final JButton eraser;
    private final JButton sender;

    public Toolbar() {
        this.eraser = new JButton("ERASE ALL");
        this.sender = new JButton("SEND");

        this.eraser.setForeground(Color.RED);
        this.sender.setForeground(Color.GREEN);
        
        this.add(eraser);
        this.add(sender);
    }

    public void requestedToEraseAll(ActionListener al) {
        this.eraser.addActionListener(al);
    }

    public void requestedToSend(ActionListener al) {
        this.sender.addActionListener(al);
    }

}
