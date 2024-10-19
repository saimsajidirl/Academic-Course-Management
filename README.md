![{AF9BE525-8BF3-4155-9DCE-138C2E017B0F}](https://github.com/user-attachments/assets/17ed0812-0ebe-4055-b109-0d6c8092571f)

ModernSOSManager - Documentation

The ModernSOSManager class is a Python-based GUI (Graphical User Interface) application built using the Tkinter and Ttk libraries with additional support from the ttkthemes package to provide a modern interface. The application acts as a study management system, helping users manage course information, including the course name, instructor, credits, schedule, and semester. It also integrates basic CRUD (Create, Read, Update, Delete) functionality with additional features like saving, loading, and sorting courses.
Main Components of the Application:

    Import Statements:
        tkinter, ttk: Used to create and configure the graphical elements.
        messagebox: Provides pop-up notifications for alerts, errors, and general messages.
        requests: Handles HTTP requests to a backend for saving and loading course data.
        ThemedTk: From the ttkthemes package, provides a more modern look for the GUI by applying themes.

    Class Definition - ModernSOSManager: The ModernSOSManager class is responsible for:
        Creating the main application window.
        Handling input from the user.
        Performing various operations on the course data, such as adding, editing, and removing courses.

Class Constructor: __init__(self)

The constructor initializes the main elements of the class:

    ThemedTk Window: Uses the "arc" theme for a modern look and feel.
    Window Configuration: The window size is set to 1200x700, and background color is adjusted.
    Semesters Dictionary: Stores information about semesters.
    Main Frames: The UI is divided into two main frames:
        Left panel for input fields and buttons.
        Right panel for displaying course information in a tree view.
    Menu Bar: Provides access to a teacher's menu with different predefined teachers and their courses.

Methods in ModernSOSManager:
1. setup_styles(self)

Configures the styles for various elements using ttk.Style. Customizes:

    Treeview: For displaying courses.
    Buttons, Labels, Entry fields, and Titles.

2. setup_left_panel(self)

Sets up the left panel, which contains input fields, buttons, and a semester selector:

    create_input_fields(self): Creates four input fields (Course Name, Instructor, Credits, Schedule) using ttk.Entry.
    create_buttons(self): Adds six buttons for various functionalities: Adding, Removing, Editing courses, Saving changes, Sorting courses, and Loading courses for the selected semester.
    create_semester_selector(self): Creates a dropdown for selecting one of eight semesters.

3. setup_right_panel(self)

Creates the right panel, which contains a ttk.Treeview to display course information in a table format:

    The treeview contains four columns: Course, Instructor, Credits, and Schedule.
    Vertical and horizontal scrollbars are added to navigate through the treeview.

4. setup_menu(self)

Creates a menu bar with a "Teachers" menu, which allows users to load predefined courses based on the selected teacher.
5. CRUD Operations:

    add_item(self): Adds a new course to the Treeview and sends the course data to a backend API using an HTTP POST request.
    remove_item(self): Removes the selected course from the Treeview.
    edit_item(self): Allows editing the selected course by loading its information back into the input fields.
    save_sos(self): Saves the current list of courses to a text file.
    sort_items(self): Sorts the courses in the Treeview by the course name.
    load_subjects(self): Loads courses from the backend API for the selected semester.

6. Helper Methods:

    clear_entry_fields(self): Clears the input fields after adding or editing a course.
    select_teacher(self, teacher_number): Loads courses associated with the selected teacher from the menu.
    show_notification(self, message, type_="info"): Displays pop-up messages for notifications or errors.

External API Communication:

The application communicates with an external API (presumably a local Flask server) to save and load course data using the requests module:

    POST requests are used to send new course data to the backend.
    GET requests are used to retrieve courses for a selected semester.

Example Workflow:

    Adding a Course:
        The user fills in the course information (Course Name, Instructor, Credits, and Schedule).
        Selects a semester from the dropdown.
        Clicks the "Add Course" button, which adds the course to the Treeview and optionally sends the data to the backend.

    Editing a Course:
        The user selects a course from the Treeview.
        Clicks the "Edit Course" button, which loads the course information back into the input fields.
        After making changes, the user can re-add the course by clicking "Add Course."

    Saving Courses:
        The user can save the entire course list by clicking "Save Changes," which writes the data to a sos.txt file.

    Loading Courses:
        The user can load courses from the backend by selecting a semester and clicking "Load Courses."

    Sorting Courses:
        Courses can be sorted alphabetically by course name by clicking the "Sort Courses" button.

Conclusion:

The ModernSOSManager class provides a comprehensive solution for managing course information in a university setting. It features an intuitive UI with CRUD functionalities, support for saving and loading data, and the ability to sort courses. With modern themes and organized layout, this tool is easy to use for both administrators and students alike.
