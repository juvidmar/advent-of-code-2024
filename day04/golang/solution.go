package main

import (
    "bufio"
    "fmt"
    "log"
    "os"
    "strings"
)

func main() {
    // Open the input file
    file, err := os.Open("input.txt")
    if err != nil {
        log.Fatalf("Failed to open input.txt: %v", err)
    }
    defer file.Close()

    // Read the grid from the file
    var grid [][]rune
    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
        line := strings.TrimSpace(scanner.Text())
        if len(line) > 0 {
            grid = append(grid, []rune(line))
        }
    }
    if err := scanner.Err(); err != nil {
        log.Fatalf("Error reading input.txt: %v", err)
    }

    n := len(grid)
    if n == 0 {
        fmt.Println("The grid is empty.")
        return
    }
    m := len(grid[0])

    // Define the valid patterns
    validPatterns := [][]rune{
        {'M', 'A', 'S'},
        {'S', 'A', 'M'},
    }

    count := 0

    // Iterate over the grid, excluding borders
    for i := 1; i < n-1; i++ {
        for j := 1; j < m-1; j++ {
            if grid[i][j] == 'A' {
                // Check Diagonal 1 (top-left to bottom-right)
                diag1 := []rune{grid[i-1][j-1], grid[i][j], grid[i+1][j+1]}
                diag1Rev := reverse(diag1)
                diag1Valid := patternMatch(diag1, validPatterns) || patternMatch(diag1Rev, validPatterns)

                // Check Diagonal 2 (top-right to bottom-left)
                diag2 := []rune{grid[i-1][j+1], grid[i][j], grid[i+1][j-1]}
                diag2Rev := reverse(diag2)
                diag2Valid := patternMatch(diag2, validPatterns) || patternMatch(diag2Rev, validPatterns)

                if diag1Valid && diag2Valid {
                    count++
                }
            }
        }
    }

    fmt.Printf("Number of X-MAS patterns: %d\n", count)
}

// Helper function to reverse a slice of runes
func reverse(s []rune) []rune {
    rev := make([]rune, len(s))
    for i := range s {
        rev[i] = s[len(s)-1-i]
    }
    return rev
}

// Helper function to check if a pattern matches any of the valid patterns
func patternMatch(s []rune, patterns [][]rune) bool {
    for _, p := range patterns {
        if string(s) == string(p) {
            return true
        }
    }
    return false
}
