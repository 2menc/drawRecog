package client.view;

import java.awt.Toolkit;

import javax.swing.*;

public class GuessPanel extends JPanel{

    private final JTextField guessField;

    public GuessPanel() {
        
        this.guessField = new JTextField((int)(Toolkit.getDefaultToolkit().getScreenSize().width/3.5));
        this.guessField.setEditable(false);
        this.guessField.setHorizontalAlignment(JTextField.CENTER);

        this.add(this.guessField);
    }

    public void setGuess(String guessClass, String confidencePercent) {
        this.guessField.setText("Guess: " + guessClass + " with " + confidencePercent + "% of confidence");
    }

    public String getGuess() {
        return this.guessField.getText();
    }
    

}
