#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdint>
#include <random>
#include <functional>

struct Player {
    int64_t efficiency;
    int32_t number;
    Player(int64_t efficiency = 0, int32_t num = 0) : efficiency(efficiency), number(num) {}
};

struct Team {
    size_t first;
    size_t last;
    int64_t sum_efficiency;
    Team(size_t first, size_t last, int64_t sum) : first(first), last(last), sum_efficiency(sum) {}
};

int64_t CountEfficiency(const std::vector<Player>& team) {
    int64_t sum = 0;
    for (const auto& elem : team) {
        sum += elem.efficiency;
    }
    return sum;
}

std::vector<Player> Read() {
    int32_t amount;
    std::cin >> amount;
    std::vector<Player> team;
    team.reserve(amount);
    for (int32_t i = 0; i < amount; ++i) {
        int64_t efficiency;
        std::cin >> efficiency;
        team.emplace_back(efficiency, i + 1);
    }
    return team;
}

void Write(const std::vector<Player>& team) {
    int64_t sum = CountEfficiency(team);
    std::cout << sum << std::endl;
    for (const auto& player : team) {
        std::cout << player.number << ' ';
    }
}

bool CompareByNumber(const Player& lhs, const Player& rhs) {
    return lhs.number < rhs.number;
}

bool CompareByEfficiency(const Player& lhs, const Player& rhs) {
    return lhs.efficiency < rhs.efficiency;
}

template<class Iterator, class Compare>
Iterator Partition(Iterator left, Iterator right, 
    typename std::iterator_traits<Iterator>::value_type pivot, Compare comparator) {
    right--;
    while (left <= right) {
        while (comparator(*left, pivot)) {
            ++left;
        }
        while (comparator(pivot, *right)) {
            --right;
        }
        if (left <= right) {
            std::swap(*left, *right);
            ++left;
            --right;
        }
    }
    return left;
}

template <class Iterator, class RandomGenerator,
        class Compare = std::less<typename std::iterator_traits<Iterator>::value_type>>
void QuickSortWithGenerator(Iterator left, Iterator right, 
    RandomGenerator& generator, Compare comparator = {}) {
    if (1 >= right - left) {
        return;
    }
    std::uniform_int_distribution<> uid(0, right - left - 1);
    auto pivot = *(left + uid(generator));
    Iterator board = Partition(left, right, pivot, comparator);
    QuickSortWithGenerator(left, board, generator, comparator);
    QuickSortWithGenerator(board, right, generator, comparator);
}

template <class Iterator, 
        class Compare = std::less<typename std::iterator_traits<Iterator>::value_type>>
void QuickSort(Iterator left, Iterator right, Compare comparator = {}) {
    std::mt19937 gen(time(0));
    QuickSortWithGenerator(left, right, gen, comparator);
}

std::vector<Player> FindOptimalTeam(std::vector<Player> team) {
    size_t amount = team.size();
    QuickSort(team.begin(), team.end(), CompareByEfficiency);
    Team res(0, 1, team[0].efficiency);
    Team max(0, 1, team[0].efficiency);
    if (amount < 2) {
        return team;
    }

    while (res.last < amount) {
        if (team[res.first].efficiency + team[res.first + 1].efficiency 
                                        >=  team[res.last].efficiency) {
            res.sum_efficiency += team[res.last].efficiency;
            if (res.sum_efficiency > max.sum_efficiency) {
                max = res;
            }
            ++res.last;
        } else {
            res.sum_efficiency -= team[res.first].efficiency;
            ++res.first;
        }
    }
    
    std::vector<Player> effective_team(team.begin() + max.first, team.begin() + max.last + 1);
    QuickSort(effective_team.begin(), effective_team.end(), CompareByNumber);
    return effective_team;
}

int main() {
    std::ios_base::sync_with_stdio(false);
    std::vector<Player> team = Read();
    std::vector<Player> effective_team = FindOptimalTeam(team);
    Write(effective_team);
    return 0;
}
