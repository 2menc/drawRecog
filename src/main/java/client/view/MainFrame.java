package client.view;

import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.Toolkit;

import javax.swing.JFrame;

/**
 * MainFrame
 */
public class MainFrame extends JFrame{

    private final Toolbar toolbar;
    private final DrawPanel canvas;
    private final GuessPanel guessPanel;

    /**
     * Constructs the main frame of the application, setting up the layout, toolbar, and drawing panel.
     * Initializes the frame size based on the screen dimensions and makes it visible.
     */
    public MainFrame() {
        this.setLayout(new BorderLayout());

        final Dimension screenDimension = Toolkit.getDefaultToolkit().getScreenSize();
        final Dimension targetDimension = new Dimension((int)(screenDimension.width/2.5), (int)(screenDimension.height/2.5));

        this.toolbar = new Toolbar();
        this.canvas = new DrawPanel();
        this.guessPanel = new GuessPanel();

        this.add(this.toolbar, BorderLayout.PAGE_START);
        this.add(this.canvas, BorderLayout.CENTER);
        this.add(this.guessPanel, BorderLayout.AFTER_LAST_LINE);

        this.setSize(targetDimension);
        this.setDefaultCloseOperation(EXIT_ON_CLOSE);
        this.setResizable(false);
        this.setVisible(true);
    }

    public DrawPanel getDrawPanel() {
        return this.canvas;
    }

    public Toolbar getToolbar() {
        return this.toolbar;
    }

    public GuessPanel getGuessPanel() {
        return this.guessPanel;
    }

}
