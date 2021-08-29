v0.5.2
- Asynchronously load video
    - MovieStim4: moved GL calls out of `loadVideo`, so that heavy
        I/O portions of this method can be processed async
    - Interleave forward/reversed playback
        When forward video is playing, reversed video is loading
        in the background. Vice versa.
    - All video is no longer loaded at the front, but just before
        each session, also interleaved with UI.

v0.5.1
- bug fixes
- Make time recording more reliable

v0.5.0
- Update notes
    - Install moviepy: https://zulko.github.io/moviepy/install.html
- Better file organization
    - OOP design leads to better encapsulation
    - Reimplemented mainloop to support rendering of both videos and the playball frames
        - `Session` class supported with state machine

v0.4.6
- Apply new connecting window to all sessions

v0.4.5
- New connecting window, threading, removed button inputs

v0.4.4
- Texts change

v0.4.3
- Texts change, make texts easier to change
- New message box between practice and block 1
- bug fix: showing between window before end block

v0.4.2
- Non full screen, but maximized

v0.4.1
- Convert to fullscreen

v0.4
- Borderless screen
- Use QDialog for message boxes
- Text update
- Parameter adjustment
- Experiment logging, excel format

0.3.1
- Change to `neu` in practice session

0.3
- Full screen, user profile size and pos correctly set
- Session alignment pattern
- Logging

0.2 Alpha
- Major refactor, framework for sessions
- Probability model
- Code refactoring

0.1 Demo
- Initial refactor, two sessions for demo purpose.