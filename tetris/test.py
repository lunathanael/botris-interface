from env import TetrisEnv

env = TetrisEnv()

game_state = env.reset()
done = False

while not done:
    # command = bot.get_next_move(game_state)
    env.render()
    command = input("Enter command: ")
    game_state, events = env.step(command)
    
    if game_state.dead:
        print("DONE")
        env.render()
        done = True
        # bot.on_game_over(game_state.score)