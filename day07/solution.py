def main():
    with open("input.txt", "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    def evaluate_expression(nums, ops):
        # Evaluate left-to-right
        # nums: list of integers
        # ops:  list of operators (same length as nums-1)
        current_val = nums[0]
        for i, op in enumerate(ops):
            next_num = nums[i+1]
            if op == '+':
                current_val = current_val + next_num
            elif op == '*':
                current_val = current_val * next_num
            else:  # op == '||'
                current_val = int(str(current_val) + str(next_num))
        return current_val

    def can_form_target(nums, target):
        # If only one number
        if len(nums) == 1:
            return nums[0] == target

        operators = ['+', '*', '||']
        n = len(nums)
        found_solution = False

        def backtrack(index, ops):
            # index: which operator slot we are filling (0-based, between nums[index] and nums[index+1])
            # ops: list of chosen operators so far
            nonlocal found_solution
            if found_solution:
                return  # Early exit if we already found a solution

            if index == n - 1:
                # All operators chosen, evaluate
                val = evaluate_expression(nums, ops)
                if val == target:
                    found_solution = True
                return

            for op in operators:
                ops.append(op)
                backtrack(index + 1, ops)
                ops.pop()
                if found_solution:
                    return

        backtrack(0, [])
        return found_solution

    total = 0
    for line in lines:
        test_value_str, nums_str = line.split(":")
        test_value = int(test_value_str.strip())
        nums = list(map(int, nums_str.strip().split()))

        if can_form_target(nums, test_value):
            total += test_value

    print(total)

if __name__ == "__main__":
    main()
