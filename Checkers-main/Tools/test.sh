#!/bin/bash

# Set the number of iterations
iterations=100

# Set the paths to your AI and the Random AI
your_ai_path="/home/phuat/CS-171/Checkers/src/checkers-python/main.py"
random_ai_path="/home/phuat/CS-171/Checkers/Tools/Sample_AIs/Poor_AI/main.py"

# Initialize counters for wins (including ties) and ties
your_wins=0
random_wins=0
ties=0

# Run the test loop
for ((i = 1; i <= iterations; i++)); do
    echo "Running test $i/$iterations..."
    result=$(python3 AI_Runner.py 8 8 3 l "$your_ai_path" "$random_ai_path")
    
    # Assuming the result is a single line with "player 1 wins", "player 2 wins", or "Tie"
    if [[ $result == *"player 1 wins"* || $result == *"Tie"* ]]; then
        ((your_wins++))
        if [[ $result == *"Tie"* ]]; then
            ((ties++))
            echo "Result $i: It's a tie!"
        else
            echo "Result $i: Your AI wins!"
        fi
    elif [[ $result == *"player 2 wins"* ]]; then
        ((random_wins++))
        echo "Result $i: Poor AI wins!"
    else
        echo "Result $i: Unexpected result! Result: $result"
    fi
done

# Calculate win rate (including ties as wins for Your AI)
win_rate=$(awk "BEGIN { printf \"%.2f\n\", $your_wins / $iterations * 100 }")

# Print results
echo "Your AI wins (including ties): $your_wins"
echo "Random AI wins: $random_wins"
echo "Number of ties: $ties"
echo "Win rate (including ties) for Your AI against Random AI: $win_rate%"