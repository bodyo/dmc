#include <algorithm>
#include <iostream>
#include <limits>
#include <fstream>
#include <set>
#include <vector>

#include "json.h"

using json = nlohmann::json;

class BranchAndBoundMethod
{
    std::vector<std::vector<int>> dist_matr_;

    std::vector<std::size_t> path_cur_;
    int path_cur_len_;

    std::vector<std::size_t> shortest_path_;
    int shortest_path_len_;

    std::set<std::size_t> free_towns_;

public:

    BranchAndBoundMethod(std::vector<std::vector<int>> const& dist_matr)
        :   dist_matr_(dist_matr),
            shortest_path_len_(std::numeric_limits<int>::max())
    {
        for (std::size_t t{}; t < dist_matr.size(); ++t)
            free_towns_.insert(t);

        push_town_with_delta_dist(0);
    }

    void find_and_print_shortest()
    {
        find_shortest();
        print_shortest();
    }

private:

    void push_town_with_delta_dist(std::size_t town, int delta_dist = 0)
    {
        path_cur_.emplace_back(town);
        free_towns_.erase(town);
        path_cur_len_ += delta_dist;
    }

    void find_shortest()
    {
        do
        {
            if (successfully_fill_better_path())
            {
                shortest_path_ = path_cur_;
                shortest_path_len_ = path_cur_len_;
            }
        }
        while (successfully_inc_back_town());
    }

    bool successfully_fill_better_path()
    {
        while (!path_is_full() && successfully_push_min_good_town());
        return path_is_full();
    }

    bool path_is_full()
    {
        return path_cur_.size() >= dist_matr_.size() + 1;
    }

    bool successfully_push_min_good_town()
    {
        return path_cur_.size() == dist_matr_.size()
            ? successfully_push_good_town(0)
            : successfully_push_good_min_free_town_not_less_than(0);
    }

    bool successfully_push_good_town(std::size_t town)
    {
        auto delta_dist = dist_matr_[path_cur_.back()][town];
        bool bool_res = path_cur_len_ + delta_dist < shortest_path_len_;

        if (bool_res)
            push_town_with_delta_dist(town, delta_dist);

        return bool_res;
    }
    //-------------------------------------------------------------------------
    bool successfully_push_good_min_free_town_not_less_than(std::size_t town_start)
    {
        return std::any_of(free_towns_.lower_bound(town_start), free_towns_.end(),
                   [&](auto town) {
                       return this->successfully_push_good_town(town);
                   });
    }
    //-------------------------------------------------------------------------
    bool successfully_inc_back_town()
    {
        return path_cur_.size() > 1 && (successfully_push_good_min_free_town_not_less_than(pop_and_get_town() + 1)
                                    || successfully_inc_back_town());
    }
    //-------------------------------------------------------------------------
    std::size_t pop_and_get_town()
    {
        auto back_town = path_cur_.back();
        path_cur_.pop_back();

        if (back_town)
            free_towns_.insert(back_town);

        auto penultimate_town = path_cur_.back();

        path_cur_len_ -= dist_matr_[penultimate_town]
                                   [back_town];

        return back_town;
    }

    void print_shortest()
    {
        std::cout << std::endl;
        for (auto town : shortest_path_)
            std::cout << town + 1 << '\t';
        std::cout << std::endl;
    }
};

int main()
{
    std::ifstream matrixJsonFile("../lab4/matrix.json");
    if (!matrixJsonFile.is_open())
        std::cout << "something go wrong";
    json json = json::parse(matrixJsonFile);

    auto matrixJson = json["matrix"];
    int i = 1;
    std::vector<std::vector<int>> dist_matr;
    for (auto city : matrixJson)
    {
        std::string number(std::to_string(i));
        std::vector<int> vectorWeight;
        for (auto weight : city[std::to_string(i++)])
        {
            if (weight == "non")
                continue;
            else
                vectorWeight.push_back(weight.get<int>());
        }
        dist_matr.push_back(std::move(vectorWeight));
    }

    BranchAndBoundMethod path(dist_matr);
    path.find_and_print_shortest();
}
