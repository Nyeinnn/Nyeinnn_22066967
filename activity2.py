import streamlit as st
import numpy as np
import time
import plotly.express as px
import pandas as pd
from io import StringIO

# Game Class
class RobotFarmingGameStreamlit:
    def __init__(self, robot_a_name="Robot A", robot_b_name="Robot B"):
        self.robot_a_name = robot_a_name
        self.robot_b_name = robot_b_name
        self.scores = {robot_a_name: 0, robot_b_name: 0}
        self.actions = {robot_a_name: None, robot_b_name: None}
        self.history = []  # Store logs

    def step(self, action_a):
        # Robot A's action comes from user input, Robot B is random
        self.actions[self.robot_a_name] = action_a
        self.actions[self.robot_b_name] = np.random.choice(["🚜 Forward", "🛑 Yield"])

        # Update scores
        if self.actions[self.robot_a_name] == "🚜 Forward" and self.actions[self.robot_b_name] == "🚜 Forward":
            self.scores[self.robot_a_name] -= 5
            self.scores[self.robot_b_name] -= 5
        elif self.actions[self.robot_a_name] == "🚜 Forward" and self.actions[self.robot_b_name] == "🛑 Yield":
            self.scores[self.robot_a_name] += 3
            self.scores[self.robot_b_name] -= 1
        elif self.actions[self.robot_a_name] == "🛑 Yield" and self.actions[self.robot_b_name] == "🚜 Forward":
            self.scores[self.robot_a_name] -= 1
            self.scores[self.robot_b_name] += 3
        elif self.actions[self.robot_a_name] == "🛑 Yield" and self.actions[self.robot_b_name] == "🛑 Yield":
            self.scores[self.robot_a_name] += 1
            self.scores[self.robot_b_name] += 1

        # Add to history
        self.history.append(
            {
                "Step": len(self.history) + 1,
                f"{self.robot_a_name} Action": self.actions[self.robot_a_name],
                f"{self.robot_b_name} Action": self.actions[self.robot_b_name],
                f"{self.robot_a_name} Score": self.scores[self.robot_a_name],
                f"{self.robot_b_name} Score": self.scores[self.robot_b_name],
            }
        )

    def get_history_dataframe(self):
        return pd.DataFrame(self.history)

# Streamlit UI
st.set_page_config(page_title="Interactive Robot Farming Game", layout="wide")

st.title("🤖🚜 Interactive Robot Farming Game")
st.write(
    "Welcome to the Robot Farming Game! Compete or cooperate with another robot to maximize your scores."
)

# Custom Robot Names
robot_a_name = st.text_input("Enter a name for Robot A (you):", "Robot A")
robot_b_name = st.text_input("Enter a name for Robot B (opponent):", "Robot B")

# Initialize Game
game = RobotFarmingGameStreamlit(robot_a_name, robot_b_name)
num_steps = st.slider("Select Number of Steps:", min_value=5, max_value=20, value=10)

# Game Loop
if st.button("Start Game 🚀"):
    placeholder_chart = st.empty()
    placeholder_logs = st.empty()
    progress_bar = st.progress(0)

    for step in range(num_steps):
        st.subheader(f"Step {step + 1} of {num_steps}")

        # User chooses action for Robot A
        action_a = st.radio(
            f"What should {robot_a_name} do?", ["🚜 Forward", "🛑 Yield"], index=0, key=f"action_{step}"
        )

        # Run a game step
        game.step(action_a)
        progress_bar.progress((step + 1) / num_steps)

        # Update chart
        scores_df = pd.DataFrame(
            {
                "Robot": [robot_a_name, robot_b_name],
                "Score": [game.scores[robot_a_name], game.scores[robot_b_name]],
            }
        )
        chart = px.bar(
            scores_df,
            x="Robot",
            y="Score",
            color="Robot",
            title="Current Robot Scores",
            text="Score",
            color_discrete_map={robot_a_name: "orange", robot_b_name: "blue"},
        )
        placeholder_chart.plotly_chart(chart, use_container_width=True)

        # Show the last 5 game logs
        logs_df = game.get_history_dataframe()
        placeholder_logs.table(logs_df.tail(5))

        # Pause for user to see the result
        time.sleep(1)

    # Game Over
    st.success("Game Over! 🎉")
    st.balloons()
    st.subheader("🏆 Final Scores")
    st.write(f"**{robot_a_name}:** {game.scores[robot_a_name]} points")
    st.write(f"**{robot_b_name}:** {game.scores[robot_b_name]} points")

    # Determine winner
    if game.scores[robot_a_name] > game.scores[robot_b_name]:
        st.success(f"🥇 Congratulations, {robot_a_name} wins! 🏆")
    elif game.scores[robot_a_name] < game.scores[robot_b_name]:
        st.error(f"😢 {robot_b_name} wins! Better luck next time.")
    else:
        st.info("🤝 It's a Tie! Great job!")

    # Download Game Logs
    st.subheader("📥 Download Game Logs")
    csv_buffer = StringIO()
    logs_df.to_csv(csv_buffer, index=False)
    st.download_button(
        label="Download Logs as CSV",
        data=csv_buffer.getvalue(),
        file_name="robot_game_logs.csv",
        mime="text/csv",
    )
