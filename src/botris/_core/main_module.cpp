#include <nanobind/nanobind.h>

namespace nb = nanobind;

void bind_piece(nb::module_ &m);
void bind_board(nb::module_ &m);
void bind_game(nb::module_ &m);
void bind_modes(nb::module_ &m);
void bind_constants(nb::module_ &m);
void bind_movegen(nb::module_ &m);

NB_MODULE(_core, m) {
    bind_piece(m);
    bind_board(m);
    bind_game(m);
    bind_modes(m);
    bind_constants(m);
    bind_movegen(m);
}
