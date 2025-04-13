#include "solver.hpp"
#include <queue>

using std::queue;

Solver::Solver() {
    Py_Initialize();
    do_move = PyObject_GetAttrString(module, "call_do_move");
}

void Solver::solve(const string& puzzle_id) {
    discover();
    propagate();
}

vector<State> Solver::getChildren(State s) const {

}

void Solver::discover() {
    State start;
    unordered_set<State> visited;
    queue<State> q;
    q.push(start);
    visited.insert(start);
    while (!q.empty()) {
        State position = q.front();
        q.pop();
        uint8_t value;
        if (value == 0) {
            rem_map.emplace(position, 0xff);
        } else if (value == 1) {
            rem_map.emplace(position, 0);
            primitives.insert(position);
        } else {
            vector<State> children = getChildren(position);
            for (State child : children) {
                if (!parent_map.contains(child)) {
                    parent_map.emplace(child, unordered_set<State>());
                }
                parent_map[child].insert(position);
                if (!visited.contains(child)) {
                    visited.insert(child);
                    q.push(child);
                }
            }
        }

    }
}

void Solver::propagate() {
    queue<State> q;
    for (State s : primitives) {
        q.push(s);
    }
    while (!q.empty()) {
        State position = q.front();
        q.pop();
        Remoteness rem = rem_map.at(position) + 1;
        unordered_set<State> parents = parent_map.at(position);
        for (State parent : parents) {
            if (!rem_map.contains(parent)) {
                rem_map.emplace(parent, rem);
                q.push(parent);
            }
        }
    }
}