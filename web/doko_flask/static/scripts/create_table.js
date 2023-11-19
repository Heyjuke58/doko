// import { transitionHiddenElement } from '@cloudfour/transition-hidden-element';

// let fade_containers = document.querySelectorAll('.fade-container');
// let transitioners = {};

// fade_containers.forEach(function (element) {
//     transitioners[element.name] = transitionHiddenElement({
//         element: element,
//         visibleClass: 'is-open',
//     });
// });


// function show(element) {
//     element.removeEventListener('transitionend', listener);
//     element.removeAttribute('hidden');

//     /**
//     * Force a browser re-paint so the browser will realize the
//     * element is no longer `hidden` and allow transitions.
//     */
//     const reflow = element.offsetHeight;

//     // Trigger our CSS transition
//     element.classList.add('is-open');
// }

// const listener = (element) => {
//     if (e.target === element) { // Match our event target to our drawer
//         element.setAttribute('hidden', true);
//         element.removeEventListener('transitionend', listener);
//     }
// };

// function hide_2(element) {
//     element.addEventListener('transitionend', listener);
//     element.classList.remove('is-open');
// }

// var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
// var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
//     return new bootstrap.Tooltip(tooltipTriggerEl)
// })

function toggle_label(label_1, label_2, label_3, label_4, check_1, check_2, check_3, check_4) {
    label_1.classList.remove("btn-outline-primary");
    label_1.classList.add("btn-primary");
    check_1.checked = true;

    let labels = [label_2, label_3, label_4];
    labels.forEach((element) => {
        if (typeof element !== "undefined") {
            element.classList.remove("btn-primary");
            element.classList.add("btn-outline-primary")
        }
    });

    let checks = [check_2, check_3, check_4];
    checks.forEach((element) => {
        if (typeof element !== "undefined") {
            element.checked = false;
        }
    });
}

var check_first_dulle = document.querySelector("input[id=first_dulle]");
var label_first_dulle = document.querySelector("label[id=label_first_dulle]");
var check_second_dulle = document.querySelector("input[id=second_dulle]");
var label_second_dulle = document.querySelector("label[id=label_second_dulle]");

check_first_dulle.addEventListener("change", function () {
    if (this.checked) {
        toggle_label(label_first_dulle, label_second_dulle, undefined, undefined,
            check_first_dulle, check_second_dulle, undefined, undefined)
    }
});
check_second_dulle.addEventListener("change", function () {
    if (this.checked) {
        toggle_label(label_second_dulle, label_first_dulle, undefined, undefined,
            check_second_dulle, check_first_dulle, undefined, undefined)
    }
});

var checkbox_announcement_plus_2 = document.querySelector("input[id=announcement_plus_2]");
var checkbox_announcement_doubles = document.querySelector("input[id=announcement_doubles]");

var label_announcement_plus_2 = document.querySelector("label[id=label_announcement_plus_2]");
var label_announcement_doubles = document.querySelector("label[id=label_announcement_doubles]");

var checkbox_also_double_extra_points = document.querySelector("input[id=also_double_extra_points]");

var container_announcement = document.querySelector("div[id=container_announcement]");

checkbox_announcement_plus_2.addEventListener("change", function () {
    if (this.checked) {
        toggle_label(label_announcement_plus_2, label_announcement_doubles, undefined, undefined,
            checkbox_announcement_plus_2, checkbox_announcement_doubles, undefined, undefined);
        hide(container_announcement, true);
        check(checkbox_also_double_extra_points, false);
    }
});
checkbox_announcement_doubles.addEventListener("change", function () {
    if (this.checked) {
        toggle_label(label_announcement_doubles, label_announcement_plus_2, undefined, undefined,
            checkbox_announcement_doubles, checkbox_announcement_plus_2, undefined, undefined);
        hide(container_announcement, false);
    }
});

function disable(object, disable) {
    if (disable) {
        object.disabled = true;
    } else {
        object.disabled = false;
    }
};

function check(object, check) {
    if (check) {
        object.checked = true;
    } else {
        object.checked = false;
    }
};

function hide(object, hide) {
    if (hide) {
        object.setAttribute("hidden", "hidden");
    } else {
        object.removeAttribute("hidden");
    }
};

var checkbox_piggies = document.querySelector("input[id=piggies]");

var checkbox_piggies_auto_announce = document.querySelector("input[id=piggies_auto_announce]");
var checkbox_piggies_in_poverty = document.querySelector("input[id=piggies_in_poverty]");
var checkbox_piggies_in_solo = document.querySelector("input[id=piggies_in_trump_and_color_solo]");

var container_piggies = document.querySelector("div[id=container_piggies]");

checkbox_piggies.addEventListener('change', function () {
    if (this.checked) {
        check(checkbox_piggies_auto_announce, false);
        check(checkbox_piggies_in_solo, false);
        check(checkbox_piggies_in_poverty, false);
        hide(container_piggies, false);
    } else {
        check(checkbox_piggies_auto_announce, true);
        check(checkbox_piggies_in_solo, true);
        check(checkbox_piggies_in_poverty, true);
        hide(container_piggies, true);
    }
});

var checkbox_trump_solo = document.querySelector("input[id=trump_solo]");

var checkbox_color_solo_pure = document.querySelector("input[id=color_solo_pure]");
var checkbox_color_solo_diamonds_replaced = document.querySelector("input[id=color_solo_diamonds_replaced]");
var checkbox_color_solo_none = document.querySelector("input[id=color_solo_none]");

var label_color_solo_pure = document.querySelector("label[id=label_pure]");
var label_color_solo_diamonds_replaced = document.querySelector("label[id=label_diamonds_replaced]");
var label_color_solo_none = document.querySelector("label[id=label_none]");

checkbox_color_solo_pure.addEventListener('change', function () {
    if (this.checked) {
        toggle_label(label_color_solo_pure, label_color_solo_diamonds_replaced, label_color_solo_none, undefined,
            checkbox_color_solo_pure, checkbox_color_solo_diamonds_replaced, checkbox_color_solo_none, undefined);
    }
    // if (this.checked && checkbox_color_solo_diamonds_replaced.checked) {
    //     check(checkbox_color_solo_diamonds_replaced, false);
    // }
    // check_piggies_solo()
});

checkbox_color_solo_diamonds_replaced.addEventListener('change', function () {
    if (this.checked) {
        toggle_label(label_color_solo_diamonds_replaced, label_color_solo_pure, label_color_solo_none, undefined,
            checkbox_color_solo_diamonds_replaced, checkbox_color_solo_pure, checkbox_color_solo_none, undefined);
    }
    // if (this.checked && checkbox_color_solo_pure.checked) {
    //     check(checkbox_color_solo_pure, false);
    // }
    // check_piggies_solo()
});

checkbox_color_solo_none.addEventListener('change', function () {
    if (this.checked) {
        toggle_label(label_color_solo_none, label_color_solo_diamonds_replaced, label_color_solo_pure, undefined,
            checkbox_color_solo_none, checkbox_color_solo_diamonds_replaced, checkbox_color_solo_pure, undefined);
    }
});

checkbox_trump_solo.addEventListener('change', function () {
    check_piggies_solo()
});

function check_piggies_solo() {
    if (!checkbox_color_solo_pure.checked && !checkbox_color_solo_diamonds_replaced.checked && !checkbox_trump_solo.checked) {
        disable(checkbox_piggies_in_solo, true);
        check(checkbox_piggies_in_solo, false);
    } else {
        disable(checkbox_piggies_in_solo, false);
    }
}

var checkbox_fox_caught = document.querySelector("input[id=fox_caught]");
var checkbox_fox_caught_in_solos = document.querySelector("input[id=fox_caught_in_solos]");
var checkbox_fox_last_trick = document.querySelector("input[id=fox_last_trick]");
var container_fox = document.querySelector("div[name=container_fox]");

checkbox_fox_caught.addEventListener('change', function () {
    if (this.checked) {
        disable(checkbox_fox_caught_in_solos, false);
        disable(checkbox_fox_last_trick, false);
        hide(container_fox, false);
    } else {
        disable(checkbox_fox_caught_in_solos, true);
        disable(checkbox_fox_last_trick, true);
        check(checkbox_fox_caught_in_solos, false);
        check(checkbox_fox_last_trick, false);
        hide(container_fox, true);
    }
});

var checkbox_dulle_caught_dulle = document.querySelector("input[id=dulle_caught_dulle]");
var checkbox_dulle_caught = document.querySelector("input[id=dulle_caught_any]");
var checkbox_dulle_caught_no = document.querySelector("input[id=dulle_caught_no]");

var label_dulle_caught_dulle = document.querySelector("label[id=label_dulle_caught_dulle]");
var label_dulle_caught = document.querySelector("label[id=label_dulle_caught_any]");
var label_dulle_caught_no = document.querySelector("label[id=label_dulle_caught_no]");

var container_dulle = document.querySelector("div[name=container_dulle]");

checkbox_dulle_caught_dulle.addEventListener("change", function () {
    if (this.checked) {
        toggle_label(label_dulle_caught_dulle, label_dulle_caught_no, label_dulle_caught, undefined,
            checkbox_dulle_caught_dulle, checkbox_dulle_caught_no, checkbox_dulle_caught, undefined);
    }
});
checkbox_dulle_caught.addEventListener("change", function () {
    if (this.checked) {
        toggle_label(label_dulle_caught, label_dulle_caught_dulle, label_dulle_caught_no, undefined,
            checkbox_dulle_caught, checkbox_dulle_caught_dulle, checkbox_dulle_caught_no, undefined);
    }
});
checkbox_dulle_caught_no.addEventListener("change", function () {
    if (this.checked) {
        toggle_label(label_dulle_caught_no, label_dulle_caught, label_dulle_caught_dulle, undefined,
            checkbox_dulle_caught_no, checkbox_dulle_caught, checkbox_dulle_caught_dulle, undefined);
    }
});

var checkbox_karlchen = document.querySelector("input[id=karlchen]");

var checkbox_karlchen_caught = document.querySelector("input[id=karlchen_caught_any_card]");
var checkbox_karlchen_caught_queen_of_diamonds = document.querySelector("input[id=karlchen_caught_queen_of_diamonds]");
var checkbox_karlchen_caught_plus = document.querySelector("input[id=karlchen_caught_plus]");
var checkbox_karlchen_caught_no = document.querySelector("input[id=karlchen_caught_no]");

var label_karlchen_caught = document.querySelector("label[id=label_karlchen_caught_any_card]");
var label_karlchen_caught_queen_of_diamonds = document.querySelector("label[id=label_karlchen_caught_queen_of_diamonds]");
var label_karlchen_caught_plus = document.querySelector("label[id=label_karlchen_caught_plus]");
var label_karlchen_caught_no = document.querySelector("label[id=label_karlchen_caught_no]");

var container_karlchen = document.querySelector("div[id=container_karlchen]");

checkbox_karlchen.addEventListener('change', function () {
    if (!this.checked) {
        hide(container_karlchen, true);
        toggle_label(label_karlchen_caught_no, label_karlchen_caught, label_karlchen_caught_plus, label_karlchen_caught_queen_of_diamonds,
            checkbox_karlchen_caught_no, checkbox_karlchen_caught, checkbox_karlchen_caught_plus, checkbox_karlchen_caught_queen_of_diamonds);
    } else {
        hide(container_karlchen, false);
    }
});

checkbox_karlchen_caught.addEventListener("change", function () {
    if (this.checked) {
        toggle_label(label_karlchen_caught, label_karlchen_caught_queen_of_diamonds, label_karlchen_caught_plus, label_karlchen_caught_no,
            checkbox_karlchen_caught, checkbox_karlchen_caught_queen_of_diamonds, checkbox_karlchen_caught_plus, checkbox_karlchen_caught_no);
    }
});

checkbox_karlchen_caught_queen_of_diamonds.addEventListener("change", function () {
    if (this.checked) {
        toggle_label(label_karlchen_caught_queen_of_diamonds, label_karlchen_caught, label_karlchen_caught_plus, label_karlchen_caught_no,
            checkbox_karlchen_caught_queen_of_diamonds, checkbox_karlchen_caught, checkbox_karlchen_caught_plus, checkbox_karlchen_caught_no);
    }
});

checkbox_karlchen_caught_plus.addEventListener("change", function () {
    if (this.checked) {
        toggle_label(label_karlchen_caught_plus, label_karlchen_caught_queen_of_diamonds, label_karlchen_caught, label_karlchen_caught_no,
            checkbox_karlchen_caught_plus, checkbox_karlchen_caught_queen_of_diamonds, checkbox_karlchen_caught, checkbox_karlchen_caught_no);
    }
});

checkbox_karlchen_caught_no.addEventListener("change", function () {
    if (this.checked) {
        toggle_label(label_karlchen_caught_no, label_karlchen_caught_plus, label_karlchen_caught_queen_of_diamonds, label_karlchen_caught,
            checkbox_karlchen_caught_no, checkbox_karlchen_caught_plus, checkbox_karlchen_caught_queen_of_diamonds, checkbox_karlchen_caught);
    }
});

var checkbox_throws = document.querySelector("input[id=throws]");

var checkbox_five_louses = document.querySelector("input[id=five_louses]");
var checkbox_fox_highest_trump = document.querySelector("input[id=fox_highest_trump]");
var checkbox_seven_fulls = document.querySelector("input[id=seven_fulls]");
var checkbox_less_than_3_trumps = document.querySelector("input[id=less_than_3_trumps]");

var container_throws = document.querySelector("div[id=container_throws]");

checkbox_throws.addEventListener("change", function () {
    if (this.checked) {
        hide(container_throws, false);
    } else {
        hide(container_throws, true);
        check(checkbox_five_louses, false);
        check(checkbox_fox_highest_trump, false);
        check(checkbox_seven_fulls, false);
        check(checkbox_less_than_3_trumps, false);
    }
});

var checkbox_any_trick = document.querySelector("input[id=any_trick]");
var checkbox_non_trump_trick = document.querySelector("input[id=non_trump_trick]");
var checkbox_trump_trick = document.querySelector("input[id=trump_trick]");
var checkbox_player_decides = document.querySelector("input[id=player_decides]");

var label_any_trick = document.querySelector("label[id=label_any_trick]");
var label_non_trump_trick = document.querySelector("label[id=label_non_trump_trick]");
var label_trump_trick = document.querySelector("label[id=label_trump_trick]");
var label_player_decides = document.querySelector("label[id=label_player_decides]");

checkbox_any_trick.addEventListener("change", function () {
    if (this.checked) {
        toggle_label(label_any_trick, label_trump_trick, label_player_decides, label_non_trump_trick,
            checkbox_any_trick, checkbox_trump_trick, checkbox_player_decides, checkbox_non_trump_trick);
    }
});
checkbox_non_trump_trick.addEventListener("change", function () {
    if (this.checked) {
        toggle_label(label_non_trump_trick, label_trump_trick, label_player_decides, label_any_trick,
            checkbox_non_trump_trick, checkbox_trump_trick, checkbox_player_decides, checkbox_any_trick);
    }
});
checkbox_trump_trick.addEventListener("change", function () {
    if (this.checked) {
        toggle_label(label_trump_trick, label_non_trump_trick, label_player_decides, label_any_trick,
            checkbox_trump_trick, checkbox_non_trump_trick, checkbox_player_decides, checkbox_any_trick);
    }
});
checkbox_player_decides.addEventListener("change", function () {
    if (this.checked) {
        toggle_label(label_player_decides, label_non_trump_trick, label_trump_trick, label_any_trick,
            checkbox_player_decides, checkbox_non_trump_trick, checkbox_trump_trick, checkbox_any_trick);
    }
});

var checkbox_overlap_bock = document.querySelector("input[id=overlap_bock]");
var checkbox_append_bock = document.querySelector("input[id=append_bock]");

var label_overlap_bock = document.querySelector("label[id=label_overlap_bock]");
var label_append_bock = document.querySelector("label[id=label_append_bock]");

checkbox_overlap_bock.addEventListener("change", function () {
    if (this.checked) {
        toggle_label(label_overlap_bock, label_append_bock, undefined, undefined,
            checkbox_overlap_bock, checkbox_append_bock, undefined, undefined);
    }
});
checkbox_append_bock.addEventListener("change", function () {
    if (this.checked) {
        toggle_label(label_append_bock, label_overlap_bock, undefined, undefined,
            checkbox_append_bock, checkbox_overlap_bock, undefined, undefined);
    }
});