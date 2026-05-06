def optimize_tasks(tasks, max_hours):

    n = len(tasks)

    dp = [[0 for _ in range(max_hours + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):

        duration = tasks[i - 1]["duration"]
        score = tasks[i - 1]["score"]

        for h in range(max_hours + 1):

            if duration <= h:

                dp[i][h] = max(
                    score + dp[i - 1][h - duration],
                    dp[i - 1][h]
                )

            else:
                dp[i][h] = dp[i - 1][h]

    selected = []

    h = max_hours

    for i in range(n, 0, -1):

        if dp[i][h] != dp[i - 1][h]:

            selected.append(tasks[i - 1])

            h -= tasks[i - 1]["duration"]

    selected.reverse()

    return {
        "selected_tasks": selected,
        "total_score": dp[n][max_hours],
        "total_duration": sum(task["duration"] for task in selected)
    }