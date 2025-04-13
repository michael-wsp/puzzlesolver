#ifndef SOLVER_H
#define SOLVER_H

#include <string>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <cstdint>
#include <Python.h>

using std::unordered_map;
using std::unordered_set;
using std::string;
using std::vector;

typedef uint32_t State;
typedef uint8_t Remoteness;

class Solver {
private:
    unordered_map<State, Remoteness> rem_map;
    unordered_map<State, unordered_set<State>> parent_map;
    unordered_set<State> primitives;
    PyObject* module;
    PyObject* do_move;
    PyObject* generate_moves;
    PyObject* primitive;

public:
    Solver();
    void solve(const string& puzzle_id);
    vector<State> getChildren(State s) const;
    void discover();
    void propagate();
};

#endif