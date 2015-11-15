# Import OctoPG
import octopg

# Load the hello_world! screen
images = octopg.res.load_images({
    "screen": "assets/sprites/hello_world_example/screen.png"
})

# This is used to know if the setup is being opened
setup = False

# When the setup has to close
def on_setup_close():
    global setup

    # Set setup as closed
    setup = False

# Infinite loop
while True:

    # Update the events
    octopg.events.update()

    # Reset the screen
    octopg.graphics.reset()

    # Setup not opened, show the hello_world! screen
    if not setup:

        # Retrieve the events
        for event in octopg.events.retrieve_events():
            # A button from a controller is down
            if event.type == octopg.events.CNTLR_KEYDOWN:
                # A select button was pressed by one of the players
                if event.btn_global == octopg.events.BTN_SELECT:
                    # Open setup
                    setup = True

        # Show the hello_world! screen
        octopg.graphics.screen.blit(images["screen"], [0, 0])

    # Else show the setup screen
    else:
        octopg.settings.loop(on_setup_close)

    # Update screen
    octopg.graphics.flip()