package client.view;

import javax.swing.*;

public class GuessPanel extends JPanel{

    private final JTextField guessField;

    public GuessPanel() {
        this.guessField = new JTextField();
    }

    public void setGuess(String guessClass, float confidencePercent) {
        this.guessField.setText("Guess: " + guessClass + "with " + confidencePercent + "% of confidence");
    }
    

}
