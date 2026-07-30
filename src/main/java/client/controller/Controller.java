package client.controller;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import client.model.ImageConverter;
import client.model.connection.Sender;
import client.view.MainFrame;

public class Controller {

    private final MainFrame mainFrame;
    private String guess;

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
                final var buffImg = ImageConverter.convertToImage(mainFrame.getDrawPanel().getDrawing(), mainFrame.getDrawPanel().getSize());
                /*
                try {
                    File outF = new File("DELETEME.png");
                    ImageIO.write(buffImg, "png", outF);
                } catch (Exception efd) {

                }
                */
                final var sender = new Sender();

                guess = sender.sendFile(buffImg);
                System.out.println(guess);
            }            
        });
    }

}
