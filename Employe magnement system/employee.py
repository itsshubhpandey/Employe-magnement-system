from datetime import date, datetime
from pathlib import Path
from tkinter import *
from tkinter import messagebox, ttk

from tkcalendar import DateEntry  # type: ignore[import]

import sqlite3

from typing import Any, Dict, List, Optional, Tuple


DB_PATH = Path(__file__).with_name("employees.db")

COLUMN_ORDER = (
    "empid",
    "name",
    "email",
    "contact",
    "gender",
    "dob",
    "doj",
    "emp_type",
    "work_shift",
    "salary",
    "education",
    "user_type",
    "address",
    "password",
)

SEARCH_FIELD_MAP = {
    "Id": "empid",
    "Name": "name",
    "Email": "email",
}


def init_db() -> None:
    DB_PATH.touch(exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS employees (
                empid TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                contact TEXT,
                gender TEXT,
                dob TEXT,
                doj TEXT,
                emp_type TEXT,
                work_shift TEXT,
                salary REAL,
                education TEXT,
                user_type TEXT,
                address TEXT,
                password TEXT
            )
            """
        )


def fetch_employees(
    search_field: Optional[str] = None,
    search_value: Optional[str] = None,
) -> List[Tuple[Any, ...]]:
    query = f"SELECT {', '.join(COLUMN_ORDER)} FROM employees"
    params: Tuple[Any, ...] = ()

    if search_field and search_value:
        query += f" WHERE {search_field} LIKE ?"
        params = (f"%{search_value}%",)

    query += " ORDER BY name COLLATE NOCASE"

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(query, params)
        return [tuple(row[col] for col in COLUMN_ORDER) for row in cursor.fetchall()]


def open_employee_frame(Window: Tk) -> None:
    init_db()

    employee_frame = Frame(Window, bg="white")
    employee_frame.place(x=0, y=0, relwidth=1, relheight=1)

    headinglabel = Label(
        employee_frame,
        text="Manage Employee Details",
        anchor="center",
        font=("Cascadia Mono", 25, "bold"),
        bg="#4A63FF",
        fg="white",
    )
    headinglabel.place(x=0, y=0, relwidth=1, height=50)

    topframe = Frame(employee_frame, bg="#4A63FF")
    topframe.place(x=0, y=50, relwidth=1, height=370)

    searchframe = Frame(topframe, bg="#4A63FF")
    searchframe.pack(pady=30)

    treeframe = Frame(topframe, bg="white")
    treeframe.pack(pady=10, padx=10, fill=BOTH, expand=True)

    horizontalScrollbar = Scrollbar(treeframe, orient=HORIZONTAL)
    verticalScrollbar = Scrollbar(treeframe, orient=VERTICAL)

    employeeTreeview = ttk.Treeview(
        treeframe,
        columns=COLUMN_ORDER,
        show="headings",
        yscrollcommand=verticalScrollbar.set,
        xscrollcommand=horizontalScrollbar.set,
    )

    detilframe = Frame(employee_frame, bg="white")
    detilframe.place(x=0, y=445, relwidth=1, height=300)

    buttonframe = Frame(employee_frame, bg="white")
    buttonframe.place(x=0, y=789, relwidth=1, height=100)

    backButton = Button(
        employee_frame,
        text="Back",
        font=("Cascadia Mono", 12, "bold"),
        bg="white",
        cursor="hand2",
        command=lambda: employee_frame.place_forget(),
    )
    backButton.place(x=10, y=10)

    search_var = StringVar(value="Id")
    search_entry_var = StringVar()
    searchCombobox = ttk.Combobox(
        searchframe,
        values=tuple(SEARCH_FIELD_MAP.keys()),
        state="readonly",
        justify="center",
        font=("Cascadia Mono", 9, "bold"),
        textvariable=search_var,
    )
    searchCombobox.grid(row=0, column=0, padx=10)

    searchentry = Entry(
        searchframe,
        font=("Cascadia Mono", 9),
        bd=0,
        bg="white",
        textvariable=search_entry_var,
    )
    searchentry.grid(row=0, column=1)

    searchButton = Button(
        searchframe,
        text="🔎 Search",
        font=("Cascadia Mono", 9, "bold"),
        bd=0,
        bg="white",
        width=11,
        cursor="hand2",
    )
    searchButton.grid(row=0, column=2, padx=12)

    showButton = Button(
        searchframe,
        text="📋 Show all",
        font=("Cascadia Mono", 9, "bold"),
        bd=0,
        bg="white",
        width=11,
        cursor="hand2",
    )
    showButton.grid(row=0, column=3)

    verticalScrollbar.pack(side=RIGHT, fill=Y)
    horizontalScrollbar.pack(side=BOTTOM, fill=X)
    employeeTreeview.pack(side=LEFT, fill=BOTH, expand=True)

    horizontalScrollbar.config(command=employeeTreeview.xview)
    verticalScrollbar.config(command=employeeTreeview.yview)

    employeeTreeview.heading("empid", text="Employee ID")
    employeeTreeview.heading("name", text="Name")
    employeeTreeview.heading("email", text="Email")
    employeeTreeview.heading("contact", text="Contact")
    employeeTreeview.heading("gender", text="Gender")
    employeeTreeview.heading("dob", text="Date of Birth")
    employeeTreeview.heading("doj", text="Date of Joining")
    employeeTreeview.heading("emp_type", text="Employment Type")
    employeeTreeview.heading("work_shift", text="Work Shift")
    employeeTreeview.heading("salary", text="Salary")
    employeeTreeview.heading("education", text="Education")
    employeeTreeview.heading("user_type", text="User Type")
    employeeTreeview.heading("address", text="Address")
    employeeTreeview.heading("password", text="Password")

    employeeTreeview.column("empid", width=90)
    employeeTreeview.column("name", width=160)
    employeeTreeview.column("email", width=200)
    employeeTreeview.column("contact", width=140)
    employeeTreeview.column("gender", width=80)
    employeeTreeview.column("dob", width=120)
    employeeTreeview.column("doj", width=120)
    employeeTreeview.column("emp_type", width=140)
    employeeTreeview.column("work_shift", width=120)
    employeeTreeview.column("salary", width=120)
    employeeTreeview.column("education", width=160)
    employeeTreeview.column("user_type", width=120)
    employeeTreeview.column("address", width=0, stretch=False)
    employeeTreeview.column("password", width=0, stretch=False)

    container = Frame(detilframe, bg="white")
    container.place(relx=0.5, rely=0.5, anchor="center")

    empid_var = StringVar()
    name_var = StringVar()
    email_var = StringVar()
    contact_var = StringVar()
    gender_var = StringVar(value="Select Gender")
    employment_type_var = StringVar(value="Select Type")
    work_shift_var = StringVar(value="Select Shift")
    salary_var = StringVar()
    education_var = StringVar()
    user_type_var = StringVar(value="Select User Type")
    password_var = StringVar()

    # --- Form Entries ---
    Label(
        container,
        text="EmpId",
        font=("Cascadia Mono", 15, "bold"),
        bg="white",
        fg="#4A63FF",
    ).grid(row=0, column=0, sticky="w", padx=(0, 15), pady=15)
    empidentry = Entry(
        container,
        font=("Cascadia Mono", 10, "bold"),
        fg="white",
        bg="#E0E4FF",
        width=20,
        textvariable=empid_var,
    )
    empidentry.grid(row=0, column=1, padx=(0, 40), pady=15)

    Label(
        container,
        text="Name",
        font=("Cascadia Mono", 15, "bold"),
        bg="white",
        fg="#4A63FF",
    ).grid(row=0, column=2, sticky="w", padx=(0, 15), pady=15)
    nameentry = Entry(
        container,
        font=("Cascadia Mono", 10, "bold"),
        fg="white",
        bg="#E0E4FF",
        width=20,
        textvariable=name_var,
    )
    nameentry.grid(row=0, column=3, padx=(0, 40), pady=15)

    Label(
        container,
        text="Email",
        font=("Cascadia Mono", 15, "bold"),
        bg="white",
        fg="#4A63FF",
    ).grid(row=0, column=4, sticky="w", padx=(0, 15), pady=15)
    emailentry = Entry(
        container,
        font=("Cascadia Mono", 10, "bold"),
        fg="white",
        bg="#E0E4FF",
        width=20,
        textvariable=email_var,
    )
    emailentry.grid(row=0, column=5, padx=0, pady=15)

    Label(
        container,
        text="Gender",
        font=("Cascadia Mono", 15, "bold"),
        bg="white",
        fg="#4A63FF",
    ).grid(row=1, column=0, sticky="w", padx=(0, 15), pady=15)
    gendercombobox = ttk.Combobox(
        container,
        values=("Male", "Female", "Other"),
        font=("Cascadia Mono", 11, "bold"),
        width=18,
        state="readonly",
        textvariable=gender_var,
    )
    gendercombobox.grid(row=1, column=1, padx=(0, 40), pady=15)

    Label(
        container,
        text="Date of Birth",
        font=("Cascadia Mono", 15, "bold"),
        bg="white",
        fg="#4A63FF",
    ).grid(row=1, column=2, sticky="w", padx=(0, 15), pady=15)
    dobdateentry = DateEntry(
        container,
        font=("Cascadia Mono", 11, "bold"),
        width=18,
        state="readonly",
        date_pattern="yyyy-mm-dd",
    )
    dobdateentry.grid(row=1, column=3, padx=(0, 40), pady=15)

    Label(
        container,
        text="Contact",
        font=("Cascadia Mono", 15, "bold"),
        bg="white",
        fg="#4A63FF",
    ).grid(row=1, column=4, sticky="w", padx=(0, 15), pady=15)
    contactentry = Entry(
        container,
        font=("Cascadia Mono", 10, "bold"),
        fg="white",
        bg="#E0E4FF",
        width=20,
        textvariable=contact_var,
    )
    contactentry.grid(row=1, column=5, padx=0, pady=15)

    Label(
        container,
        text="Employment Type",
        font=("Cascadia Mono", 15, "bold"),
        bg="white",
        fg="#4A63FF",
    ).grid(row=2, column=0, sticky="w", padx=(0, 15), pady=15)
    employment_typecombobox = ttk.Combobox(
        container,
        values=("Full Time", "Part Time", "Contractual", "Casual", "Intern"),
        font=("Cascadia Mono", 11, "bold"),
        width=18,
        state="readonly",
        textvariable=employment_type_var,
    )
    employment_typecombobox.grid(row=2, column=1, padx=(0, 40), pady=15)

    Label(
        container,
        text="Work Shift",
        font=("Cascadia Mono", 15, "bold"),
        bg="white",
        fg="#4A63FF",
    ).grid(row=2, column=2, sticky="w", padx=(0, 15), pady=15)
    workshiftcombobox = ttk.Combobox(
        container,
        values=("Morning", "Evening", "Night"),
        font=("Cascadia Mono", 11, "bold"),
        width=18,
        state="readonly",
        textvariable=work_shift_var,
    )
    workshiftcombobox.grid(row=2, column=3, padx=(0, 40), pady=15)

    Label(
        container,
        text="Salary",
        font=("Cascadia Mono", 15, "bold"),
        bg="white",
        fg="#4A63FF",
    ).grid(row=2, column=4, sticky="w", padx=(0, 15), pady=15)
    salaryentry = Entry(
        container,
        font=("Cascadia Mono", 10, "bold"),
        fg="white",
        bg="#E0E4FF",
        width=20,
        textvariable=salary_var,
    )
    salaryentry.grid(row=2, column=5, padx=0, pady=15)

    Label(
        container,
        text="Address",
        font=("Cascadia Mono", 15, "bold"),
        bg="white",
        fg="#4A63FF",
    ).grid(row=3, column=0, sticky="nw", padx=(0, 15), pady=15)
    addresstext = Text(
        container,
        font=("Cascadia Mono", 10, "bold"),
        fg="white",
        bg="#E0E4FF",
        width=21,
        height=5,
    )
    addresstext.grid(row=3, column=1, padx=(0, 40), pady=10, rowspan=3)

    Label(
        container,
        text="Date of Joining",
        font=("Cascadia Mono", 15, "bold"),
        bg="white",
        fg="#4A63FF",
    ).grid(row=3, column=2, sticky="w", padx=(0, 15), pady=15)
    dojdateentry = DateEntry(
        container,
        font=("Cascadia Mono", 11, "bold"),
        width=18,
        state="readonly",
        date_pattern="yyyy-mm-dd",
    )
    dojdateentry.grid(row=3, column=3, padx=(0, 40), pady=10)

    Label(
        container,
        text="Education",
        font=("Cascadia Mono", 15, "bold"),
        bg="white",
        fg="#4A63FF",
    ).grid(row=3, column=4, sticky="w", padx=(0, 15), pady=15)
    educationentry = Entry(
        container,
        font=("Cascadia Mono", 10, "bold"),
        fg="white",
        bg="#E0E4FF",
        width=20,
        textvariable=education_var,
    )
    educationentry.grid(row=3, column=5, padx=0, pady=15)

    Label(
        container,
        text="User Type",
        font=("Cascadia Mono", 15, "bold"),
        bg="white",
        fg="#4A63FF",
    ).grid(row=4, column=2, sticky="w", padx=(0, 15), pady=15)
    usertypecombobox = ttk.Combobox(
        container,
        values=("Admin", "Employee"),
        font=("Cascadia Mono", 11, "bold"),
        width=18,
        state="readonly",
        textvariable=user_type_var,
    )
    usertypecombobox.grid(row=4, column=3, padx=(0, 40), pady=15)

    Label(
        container,
        text="Password",
        font=("Cascadia Mono", 15, "bold"),
        bg="white",
        fg="#4A63FF",
    ).grid(row=4, column=4, padx=(0, 15), pady=15, sticky="w")
    passwordentry = Entry(
        container,
        font=("Cascadia Mono", 10, "bold"),
        fg="white",
        bg="#E0E4FF",
        width=20,
        show="*",
        textvariable=password_var,
    )
    passwordentry.grid(row=4, column=5, padx=0, pady=15)

    button_container = Frame(buttonframe, bg="white")
    button_container.place(relx=0.5, rely=0.5, anchor="center")

    addButton = Button(
        button_container,
        text="➕ Add",
        font=("Cascadia Mono", 11, "bold"),
        bd=0,
        bg="#4A63FF",
        width=10,
        cursor="hand2",
        fg="white",
    )
    addButton.grid(row=0, column=0, padx=20)

    updateButton = Button(
        button_container,
        text="👍 Update",
        font=("Cascadia Mono", 11, "bold"),
        bd=0,
        bg="#4A63FF",
        width=10,
        cursor="hand2",
        fg="white",
    )
    updateButton.grid(row=0, column=1, padx=20)

    deleteButton = Button(
        button_container,
        text="🗑 Delete",
        font=("Cascadia Mono", 11, "bold"),
        bd=0,
        bg="#4A63FF",
        width=10,
        cursor="hand2",
        fg="white",
    )
    deleteButton.grid(row=0, column=2, padx=20)

    clearButton = Button(
        button_container,
        text="✏ Clear",
        font=("Cascadia Mono", 11, "bold"),
        bd=0,
        bg="#4A63FF",
        width=10,
        cursor="hand2",
        fg="white",
    )
    clearButton.grid(row=0, column=3, padx=20)

    def reset_date(entry: DateEntry) -> None:
        entry.set_date(date.today())

    def clear_form() -> None:
        empid_var.set("")
        name_var.set("")
        email_var.set("")
        contact_var.set("")
        gender_var.set("Select Gender")
        employment_type_var.set("Select Type")
        work_shift_var.set("Select Shift")
        salary_var.set("")
        education_var.set("")
        user_type_var.set("Select User Type")
        password_var.set("")
        addresstext.delete("1.0", END)
        reset_date(dobdateentry)
        reset_date(dojdateentry)
        employeeTreeview.selection_remove(*employeeTreeview.selection())

    def get_form_data() -> Dict[str, Optional[Any]]:
        data: Dict[str, Optional[Any]] = {
            "empid": empid_var.get().strip(),
            "name": name_var.get().strip(),
            "email": email_var.get().strip(),
            "contact": contact_var.get().strip() or None,
            "gender": None if gender_var.get().startswith("Select") else gender_var.get(),
            "dob": dobdateentry.get_date().isoformat(),
            "doj": dojdateentry.get_date().isoformat(),
            "emp_type": None if employment_type_var.get().startswith("Select") else employment_type_var.get(),
            "work_shift": None if work_shift_var.get().startswith("Select") else work_shift_var.get(),
            "salary": None,
            "education": education_var.get().strip() or None,
            "user_type": None if user_type_var.get().startswith("Select") else user_type_var.get(),
            "address": addresstext.get("1.0", END).strip() or None,
            "password": password_var.get() or None,
        }

        salary_raw = salary_var.get().strip()
        if salary_raw:
            try:
                data["salary"] = float(salary_raw)
            except ValueError as exc:
                raise ValueError("Salary must be a valid number.") from exc

        return data

    def refresh_treeview(records: Optional[List[Tuple[Any, ...]]] = None) -> None:
        employeeTreeview.delete(*employeeTreeview.get_children())
        if records is None:
            records = fetch_employees()

        for row in records:
            display_row = [value if value is not None else "" for value in row]
            employeeTreeview.insert("", END, values=display_row)

    def on_add() -> None:
        try:
            data = get_form_data()
        except ValueError as error:
            messagebox.showerror("Invalid Input", str(error), parent=employee_frame)
            return

        if not data["empid"] or not data["name"] or not data["email"]:
            messagebox.showerror(
                "Missing Information",
                "Employee ID, Name, and Email are required.",
                parent=employee_frame,
            )
            return

        with sqlite3.connect(DB_PATH) as conn:
            try:
                conn.execute(
                    f"""
                    INSERT INTO employees ({', '.join(COLUMN_ORDER)})
                    VALUES ({', '.join(['?'] * len(COLUMN_ORDER))})
                    """,
                    tuple(data[column] for column in COLUMN_ORDER),
                )
            except sqlite3.IntegrityError:
                messagebox.showerror(
                    "Duplicate Employee",
                    f"Employee ID '{data['empid']}' already exists.",
                    parent=employee_frame,
                )
                return

        messagebox.showinfo("Success", "Employee added successfully.", parent=employee_frame)
        refresh_treeview()
        clear_form()

    def on_update() -> None:
        try:
            data = get_form_data()
        except ValueError as error:
            messagebox.showerror("Invalid Input", str(error), parent=employee_frame)
            return

        if not data["empid"]:
            messagebox.showerror(
                "No Selection",
                "Select an employee from the table before updating.",
                parent=employee_frame,
            )
            return

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.execute(
                """
                UPDATE employees
                   SET name = ?,
                       email = ?,
                       contact = ?,
                       gender = ?,
                       dob = ?,
                       doj = ?,
                       emp_type = ?,
                       work_shift = ?,
                       salary = ?,
                       education = ?,
                       user_type = ?,
                       address = ?,
                       password = ?
                 WHERE empid = ?
                """,
                (
                    data["name"],
                    data["email"],
                    data["contact"],
                    data["gender"],
                    data["dob"],
                    data["doj"],
                    data["emp_type"],
                    data["work_shift"],
                    data["salary"],
                    data["education"],
                    data["user_type"],
                    data["address"],
                    data["password"],
                    data["empid"],
                ),
            )

        if cursor.rowcount == 0:
            messagebox.showwarning(
                "Not Found",
                "Employee not found. It may have been deleted.",
                parent=employee_frame,
            )
            return

        messagebox.showinfo("Success", "Employee updated successfully.", parent=employee_frame)
        refresh_treeview()
        clear_form()

    def on_delete() -> None:
        empid = empid_var.get().strip()
        if not empid:
            messagebox.showerror(
                "No Selection",
                "Select an employee from the table before deleting.",
                parent=employee_frame,
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete employee '{empid}'?",
            parent=employee_frame,
        )
        if not confirm:
            return

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.execute("DELETE FROM employees WHERE empid = ?", (empid,))

        if cursor.rowcount == 0:
            messagebox.showwarning(
                "Not Found",
                "Employee not found. It may have been deleted already.",
                parent=employee_frame,
            )
            return

        messagebox.showinfo("Deleted", "Employee deleted successfully.", parent=employee_frame)
        refresh_treeview()
        clear_form()

    def on_tree_select(_: object) -> None:
        selection = employeeTreeview.focus()
        if not selection:
            return

        values = employeeTreeview.item(selection, "values")
        if not values:
            return

        empid_var.set(values[0])
        name_var.set(values[1])
        email_var.set(values[2])
        contact_var.set(values[3])
        gender_var.set(values[4] or "Select Gender")

        if values[5]:
            try:
                dobdateentry.set_date(datetime.fromisoformat(values[5]))
            except ValueError:
                reset_date(dobdateentry)
        else:
            reset_date(dobdateentry)

        if values[6]:
            try:
                dojdateentry.set_date(datetime.fromisoformat(values[6]))
            except ValueError:
                reset_date(dojdateentry)
        else:
            reset_date(dojdateentry)

        employment_type_var.set(values[7] or "Select Type")
        work_shift_var.set(values[8] or "Select Shift")
        salary_var.set("" if values[9] in ("", None) else str(values[9]))
        education_var.set(values[10] or "")
        user_type_var.set(values[11] or "Select User Type")
        addresstext.delete("1.0", END)
        addresstext.insert("1.0", values[12] or "")
        password_var.set(values[13] or "")

    def on_search() -> None:
        field_key = search_var.get()
        field_name = SEARCH_FIELD_MAP.get(field_key)
        search_value = search_entry_var.get().strip()

        if not field_name:
            messagebox.showerror("Invalid Search", "Select a valid field to search.", parent=employee_frame)
            return

        if not search_value:
            messagebox.showerror("Missing Query", "Enter a value to search for.", parent=employee_frame)
            return

        records = fetch_employees(field_name, search_value)
        refresh_treeview(records)

    def on_show_all() -> None:
        search_entry_var.set("")
        refresh_treeview()

    searchButton.config(command=on_search)
    showButton.config(command=on_show_all)
    addButton.config(command=on_add)
    updateButton.config(command=on_update)
    deleteButton.config(command=on_delete)
    clearButton.config(command=clear_form)

    employeeTreeview.bind("<<TreeviewSelect>>", on_tree_select)

    clear_form()
    refresh_treeview()


