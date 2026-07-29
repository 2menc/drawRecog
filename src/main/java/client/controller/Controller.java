package client.controller;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import client.view.MainFrame;

public class Controller {

    private final MainFrame mainFrame;

    public Controller() {

        this.mainFrame = new MainFrame();

        //? LISTENERS
        this.mainFrame.getToolbar().requestedToEraseAll(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                mainFrame.getDrawPanel().eraseAll();
            }            
        });
        this.mainFrame.getToolbar().requestedToSend(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                // TODO Auto-generated method stub
                throw new UnsupportedOperationException("Unimplemented method 'actionPerformed'");
            }            
        });
    }

}
