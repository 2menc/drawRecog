package client.controller;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.List;

import client.model.ImageConverter;
import client.model.connection.NetworkClient;
import client.view.MainFrame;
import client.model.FileReader;

public class Controller {

    private final MainFrame mainFrame;
    private String guess;

    public Controller() {

        this.mainFrame = new MainFrame();

        final List<String> models = FileReader.getListFromFile("models");
        this.mainFrame.getToolbar().populateModelsCombo(models);

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

                final var client = new NetworkClient();
                
                guess = client.sendAndReceiveImage(buffImg);

                String[] guessArray = guess.split(":");

                var guessClass = guessArray[0];
                var guessConfidence = guessArray[1];

                mainFrame.getGuessPanel().setGuess(guessClass, guessConfidence);
            }            
        });
        this.mainFrame.getToolbar().requestedToChangeModel(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {

                final var client = new NetworkClient();

                final String chosenModel = mainFrame.getToolbar().getChosenModel();
                final String chosenModelCheck = client.sendAndReceiveModelChange(chosenModel);

                if (! chosenModel.equals(chosenModelCheck)) {
                    mainFrame.showErrorDialog(new IllegalStateException("model not changed correctly"));
                    return;
                }

                mainFrame.getGuessPanel().setInformation("model correctly changed in: " + chosenModelCheck);
            }            
        });

    }

}
