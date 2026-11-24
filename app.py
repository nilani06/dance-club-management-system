import streamlit as st
import pandas as pd

# ==========================
# LOAD DATA
# ==========================

students_df = pd.read_csv("students.csv")

students_df.columns = students_df.columns.str.strip()

students_df["Grade"] = students_df["Grade"].fillna("Not Assigned")
students_df["Student Name"] = students_df["Student Name"].fillna("Unknown")
students_df["Total Points"] = students_df["Total Points"].fillna(0)

# ==========================
# PAGE TITLE
# ==========================

st.title("💃 Dance Club Management System")
# ==========================
# ADMIN LOGIN
# ==========================

password = st.text_input(
    "Teacher/Admin Password",
    type="password"
)

admin_mode = password == "danceclub2026"

if admin_mode:

    st.header("👥 Student Management")

    # Add Student
    # Delete Student
    # Edit Student

else:

    st.info("Student View Mode")

# ==========================
# STUDENT MANAGEMENT
# ==========================

with st.expander("➕ Add New Student"):

    new_name = st.text_input("Student Name")

    new_grade = st.selectbox(
        "Grade",
        [
            "7A","7B","7C","7D","7E","7F",
            "8A","8B","8C","8D","8E","8F",
            "9A","9B","9C","9D","9E","9F",
            "10A","10B","10C","10D","10E","10F",
            "11A","11B","11C","11D","11E","11F",
            "12A","12B","12C","12D","12E","12F",
            "13A","13B","13C","13D","13E","13F"
        ]
    )

    if st.button("Add Student"):

        if new_name.strip() != "":

            new_student = pd.DataFrame({
                "Grade": [new_grade],
                "Student Name": [new_name],
                "Total Points": [0]
            })

            if new_name in students_df["Student Name"].values:
                st.error("Student already exists")

            students_df = pd.concat(
                [students_df, new_student],
                ignore_index=True
            )

            students_df.to_csv(
                "students.csv",
                index=False
            )

            st.success("Student Added Successfully!")
            st.rerun()

with st.expander("🗑 Delete Student"):

    delete_student = st.selectbox(
        "Select Student To Delete",
        sorted(students_df["Student Name"].tolist())
    )

    if st.button("Delete Student"):

        students_df = students_df[
            students_df["Student Name"] != delete_student
        ]

        students_df.to_csv(
            "students.csv",
            index=False
        )

        st.success("Student Deleted Successfully!")
        st.rerun()

st.divider()

with st.expander("✏️ Edit Student"):

    student_to_edit = st.selectbox(
        "Select Student To Edit",
        sorted(students_df["Student Name"].tolist())
    )

    row = students_df[
        students_df["Student Name"] == student_to_edit
    ].index[0]

    edit_grade = st.text_input(
        "Grade",
        value=str(students_df.at[row, "Grade"])
    )

    edit_name = st.text_input(
        "Student Name",
        value=str(students_df.at[row, "Student Name"])
    )

    edit_points = st.number_input(
        "Total Points",
        value=int(students_df.at[row, "Total Points"])
    )

    if st.button("Save Changes"):

        students_df.at[row, "Grade"] = edit_grade
        students_df.at[row, "Student Name"] = edit_name
        students_df.at[row, "Total Points"] = edit_points

        students_df.to_csv(
            "students.csv",
            index=False
        )

        st.success("Student Updated Successfully!")

        st.rerun()

# ==========================
# STUDENT INFORMATION
# ==========================

st.header("📋 Student Information")

student_name = st.selectbox(
    "Select Student",
    sorted(students_df["Student Name"].tolist())
)

student_data = students_df[
    students_df["Student Name"] == student_name
]

grade = str(student_data.iloc[0]["Grade"])
current_points = int(student_data.iloc[0]["Total Points"])

leaderboard_rank = students_df.sort_values(
    by="Total Points",
    ascending=False
).reset_index(drop=True)

rank = (
    leaderboard_rank[
        leaderboard_rank["Student Name"] == student_name
    ].index[0]
    + 1
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Grade", grade)

with col2:
    st.metric("Current Points", current_points)

with col3:
    st.metric("Rank", f"#{rank}")

new_student = pd.DataFrame({
    "Grade": [new_grade],
    "Student Name": [new_name],
    "Total Points": [0],
    "Most Punctual": [0],
    "Best Warm-Up": [0],
    "Best Attire": [0],
    "Most Prepared": [0]
})

st.divider()

# ==========================
# SESSION POINTS CALCULATOR
# ==========================

if admin_mode:

    st.header("🧮 Session Points Calculator")

    punctuality = st.selectbox(
        "Punctuality",
        [
            "Early",
            "On Time",
            "Late (2:31-2:40)",
            "Late (2:41+)",
            "Leaving Without Informing"
        ]
    )

    attendance = st.selectbox(
        "Attendance",
        [
            "Excused (Previous Day)",
            "Excused (On The Day)",
            "Not Excused"
        ]
    )
    
    stretching = st.selectbox(
        "Stretching",
        [
            "Warmed Up",
            "Not Warmed Up"
        ]
    )
    
    attire = st.selectbox(
        "Attire",
        [
            "Correct Attire",
            "Wrong Attire"
        ]
    )
    
    phone = st.selectbox(
        "Phone Rule",
        [
            "Followed The Rule",
            "Haven't"
        ]
    )
    
    preparedness = st.selectbox(
        "Preparedness",
        [
            "Prepared",
            "Not Prepared"
        ]
    )
    
    event = st.selectbox(
        "Event Commitment",
        [
            "None",
            "Participated",
            "Bailed"
        ]
    )
    
    if st.button("Calculate Session Points"):
    
        total = 0
    
        punctuality_points = 0
        warmup_points = 0
        attire_points = 0
        preparedness_points = 0
    
        # Punctuality
        if punctuality == "Early":
            punctuality_points = 5
    
        elif punctuality == "On Time":
            punctuality_points = 3
    
        elif punctuality == "Late (2:31-2:40)":
            punctuality_points = -3

        elif punctuality == "Late (2:41+)":
            punctuality_points = -5
    
        elif punctuality == "Leaving Without Informing":
            punctuality_points = -5
    
        total += punctuality_points
    
        # Attendance
    
        if attendance == "Excused (On The Day)":
            total -= 3
    
        elif attendance == "Not Excused":
            total -= 5
    
        # Stretching
    
        if stretching == "Warmed Up":
            warmup_points = 2
        else:
            warmup_points = -2

        total += warmup_points
    
        # Attire
    
        if attire == "Correct Attire":
            attire_points = 2
        else:
            attire_points = -2
    
        total += attire_points
    
        # Phone Rule
    
        if phone == "Followed The Rule":
            total += 2
        else:
            total -= 5
    
        # Preparedness
    
        if preparedness == "Prepared":
            preparedness_points = 3
        else:
            preparedness_points = -3
    
        total += preparedness_points
    
    # update csv
        row = students_df[
            students_df["Student Name"] == student_name
        ].index[0]
    
        students_df.at[row, "Total Points"] += total
    
        students_df.at[row, "Most Punctual"] += punctuality_points
    
        students_df.at[row, "Best Warm-Up"] += warmup_points
    
        students_df.at[row, "Best Attire"] += attire_points
    
        students_df.at[row, "Most Prepared"] += preparedness_points
    
        students_df.to_csv(
            "students.csv",
            index=False
        )
    
        new_total = students_df.at[row, "Total Points"]
    
        st.success(
            f"✅ {student_name} has been updated successfully!"
        )
    
        st.write("### Session Summary")
    
        st.write(f"Session Points Earned: {total}")
    
        st.write(f"New Total Points: {new_total}")
    
        st.write(
            f"🏃 Most Punctual: "
            f"{students_df.at[row, 'Most Punctual']}"
        )
    
        st.write(
            f"🧘 Best Warm-Up: "
            f"{students_df.at[row, 'Best Warm-Up']}"
        )
    
        st.write(
            f"👕 Best Attire: "
            f"{students_df.at[row, 'Best Attire']}"
        )
    
        st.write(
            f"📚 Most Prepared: "
            f"{students_df.at[row, 'Most Prepared']}"
        )
    
        st.balloons()
    
        st.rerun()
    
    st.divider()
    
    st.header("↩️ Undo / Manual Correction")
    
    undo_student = st.selectbox(
        "Select Student",
        sorted(students_df["Student Name"].tolist()),
        key="undo_student"
    )
    
    undo_total = st.number_input(
        "Adjust Total Points",
        value=0
    )
    
    undo_punctual = st.number_input(
        "Adjust Most Punctual",
        value=0,
        key="undo_punctual"
    )
    
    undo_warmup = st.number_input(
        "Adjust Best Warm-Up",
        value=0,
        key="undo_warmup"
    )
    
    undo_attire = st.number_input(
        "Adjust Best Attire",
        value=0,
        key="undo_attire"
    )
    
    undo_prepared = st.number_input(
        "Adjust Most Prepared",
        value=0,
        key="undo_prepared"
    )
    
    if st.button("Apply Correction"):
    
        row = students_df[
            students_df["Student Name"] == undo_student
        ].index[0]
    
        students_df.at[row, "Total Points"] += undo_total
    
        students_df.at[row, "Most Punctual"] += undo_punctual
    
        students_df.at[row, "Best Warm-Up"] += undo_warmup
    
        students_df.at[row, "Best Attire"] += undo_attire
    
        students_df.at[row, "Most Prepared"] += undo_prepared
    
        students_df.to_csv(
            "students.csv",
            index=False
        )
    
        st.success(
            f"✅ Corrections applied to {undo_student}"
        )
    
        st.rerun()
    
    st.divider()

# ==========================
# LEADERSHIP POSITIONS
# ==========================

st.header("👑 Leadership Positions")

grade10 = students_df[
    students_df["Grade"].fillna("").astype(str).str.startswith("10")
]

grade11 = students_df[
    students_df["Grade"].fillna("").astype(str).str.startswith("11")
]

if not grade10.empty:

    junior_leader = grade10.loc[
        grade10["Total Points"].idxmax()
    ]

    st.success(
        f"⭐ Junior Leader (Grade 10): "
        f"{junior_leader['Student Name']} "
        f"({junior_leader['Total Points']} pts)"
    )

if not grade11.empty:

    senior_leader = grade11.loc[
        grade11["Total Points"].idxmax()
    ]

    st.success(
        f"👑 Senior Leader (Grade 11): "
        f"{senior_leader['Student Name']} "
        f"({senior_leader['Total Points']} pts)"
    )

st.divider()

# ==========================
# SPECIAL RECOGNITION AWARDS
# ==========================

st.header("🏆 Special Recognition Awards")

max_punctual = students_df["Most Punctual"].max()

most_punctual = ", ".join(
    students_df[
        students_df["Most Punctual"] == max_punctual
    ]["Student Name"]
)

max_warmup = students_df["Best Warm-Up"].max()
best_warmup = ", ".join(
    students_df[
        students_df["Best Warm-Up"] == max_warmup
    ]["Student Name"]
)

max_attire = students_df["Best Attire"].max()
best_attire = ", ".join(
    students_df[
        students_df["Best Attire"] == max_attire
    ]["Student Name"]
)

max_prepared = students_df["Most Prepared"].max()
most_prepared = ", ".join(
    students_df[
        students_df["Most Prepared"] == max_prepared
    ]["Student Name"]
)

max_total = students_df["Total Points"].max()
overall_top = ", ".join(
    students_df[
        students_df["Total Points"] == max_total
    ]["Student Name"]
)

st.info(f"🏃 Most Punctual: {most_punctual}")
st.info(f"🧘 Best Warm-Up: {best_warmup}")
st.info(f"👕 Best Attire: {best_attire}")
st.info(f"📚 Most Prepared: {most_prepared}")
st.info(f"🌟 Overall Top Performer: {overall_top}")
