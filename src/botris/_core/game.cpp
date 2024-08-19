#include <nanobind/nanobind.h>
#include <nanobind/stl/optional.h>
#include <nanobind/stl/variant.h>
#include <nanobind/stl/array.h>
#include "engine/Game.hpp"
#include "engine/Piece.hpp"
#include "engine/MoveGen.hpp"
#include "engine/Board.hpp"
#include "engine/modes/TetrioS1.hpp"
#include "engine/modes/Botris.hpp"

namespace nb = nanobind;
using namespace nb::literals;

void bind_game(nb::module_ &m) {
    nb::class_<Game>(m, "Game")
        .def_ro_static("QUEUE_SIZE", &QUEUE_SIZE)

        .def(nb::init<>())
        .def("place_piece", nb::overload_cast<>(&Game::place_piece))
        .def("place_piece", nb::overload_cast<const Piece&>(&Game::place_piece), "piece"_a)
        .def("do_hold", &Game::do_hold)
        .def("add_garbage", &Game::add_garbage, "lines"_a, "location"_a)
        .def("damage_sent", &Game::damage_sent, "linesCleared"_a, "spinType"_a, "pc"_a)
        .def("process_movement", &Game::process_movement, "piece"_a, "movement"_a)
        .def("get_possible_piece_placements", &Game::get_possible_piece_placements)
        .def_rw("board", &Game::board)
        .def_rw("current_piece", &Game::current_piece)
        .def_rw("hold", &Game::hold)
        .def_rw("garbage_meter", &Game::garbage_meter)
        .def_rw("b2b", &Game::b2b)
        .def_rw("combo", &Game::combo)
        .def_rw("queue", &Game::queue)
        .def_rw("mode", &Game::mode)

        .def("copy", [](const Game &self) {
            Game copy = self;
            return copy;
        });
}
