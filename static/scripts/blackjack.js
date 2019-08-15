$(document).ready(function(){

    const hit = $("#hit");
    const more = $("#more");
    const money = $("#money")
    const bet = $("#bet")
    const stand = $("#stand")
    const less = $("#less")
    const game_result = $("#game-result")
    const game_finish = $(".game-finish")
    const double = $("#double")
    const deal =  $("#deal")
    const player_total = $(".player-total")
    const dealer_total = $(".dealer-total")
    const game_buttons = $(".game-buttons")

    var csrftoken = Cookies.get('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    more.click(function() {
        let fund = parseInt(money.text());
        if (fund >= 10) {
            money.text(fund - 10);
            let bet_value = parseInt(bet.text())
            bet.text(bet_value + 10);
        } else {
            alert('You need to have at least 10 coins');
        }
    }),
    less.click(function() {
        let bet_value = parseInt(bet.text());
        let minus = 10;
        if (bet >= 0 && bet_value < minus)
            minus = bet_value;
        bet.text(bet_value - minus);
        let fund = parseInt(money.text())
        money.text(fund + minus);
    });
    hit.click(function() {
        take_new_card('False', ".player-cards", ".player-total", false);
    });
    function take_new_card(to_dealer, cards_class, total_class, from_double) {
        $.ajax({
            url: '/api/card',
            type: 'POST',
            data: {
                'gameId': sessionStorage.getItem('game_id'),
                'toDealer': to_dealer
            },
            dataType: 'json',
            success: function(card) {
                card_class = fromValue(card.value) + "-of-" + card.type + "s"
                $(cards_class +  " .new-cards").append("<div class='card " + card_class + "'></div>");
                let width = parseInt($(cards_class).css("width"));
                $(cards_class).css({"width": (width + 84).toString()})
                setTotalIn(total_class, to_dealer, true, from_double)
            },
            error: function(e) {
                alert('Internal server error!')
            }
        });
    }
    function won() {
        hit.attr('disabled', 'disabled');
        stand.attr('disabled', 'disabled');

        game_result.text('You won!');
        game_finish.css({'display': 'inline-block'});

        money.text(parseInt(money.text()) + parseInt(bet.text()));
    }
    function lost() {
        hit.attr('disabled', 'disabled');
        stand.attr('disabled', 'disabled');

        game_result.text('You lost!');
        game_finish.css({'display': 'inline-block'});

        bet.text("0");
    }
    function draw() {
        hit.attr('disabled', 'disabled');
        stand.attr('disabled', 'disabled');

        game_result.text('Draw!');
        game_finish.css({'display': 'inline-block'});
    }
    stand.click(function() {
        hit.attr('disabled', 'disabled');
        stand.attr('disabled', 'disabled');

        playDealer();
    });
    function checkWinner() {
        let dealerTotal = parseInt(dealer_total.text());
        let playerTotal = parseInt(player_total.text());
        if (dealerTotal > 21 || dealerTotal < playerTotal) {
            won();
        } else if (playerTotal == dealerTotal && dealerTotal == 21) {
            draw();
        } else if (playerTotal == dealerTotal) {
            draw();
        } else {
            lost();
        }
    }
    $("#new-game").click(function() {
        game_finish.css({'display': 'none'});
        game_buttons.css({'display': 'none'});
        hit.removeAttr('disabled');
        stand.removeAttr('disabled');
        less.removeAttr('disabled');
        more.removeAttr('disabled');
        deal.css({'display': 'inline-block'});

        $(".new-cards").empty();
        $(".player-cards .card1").removeClass().addClass('card').addClass('card1').addClass("flipped");
        $(".player-cards .card2").removeClass().addClass('card').addClass('card2').addClass("flipped");
        $(".dealer-cards .card1").removeClass().addClass('card').addClass('card1').addClass("flipped");
        $(".dealer-cards .card2").removeClass().addClass('card').addClass('card2').addClass("flipped");
        $(".player-cards").css({"width": (164).toString()})
        $(".dealer-cards").css({"width": (164).toString()})

        player_total.text("0");
        dealer_total.text("0");
    });
    double.click(function() {
        let bet = parseInt(bet.text());
        let fund = parseInt(money.text());
        if (bet > fund) {
            alert('You have not enough money!');
        } else {
            bet.text(2 * bet);
            money.text(fund - bet);
            double.attr('disabled', 'disabled');
            hit.attr('disabled', 'disabled');
            stand.attr('disabled', 'disabled');
            $("#split").attr('disabled', 'disabled');

            take_new_card('False', ".player-cards", ".player-total", true);
        }
    });
    function sleep (time) {
        return new Promise((resolve) => setTimeout(resolve, time));
    }
    deal.click(function() {
        let bet = parseInt(bet.text());
        if (bet < 10) {
            alert("Mininum bet is 10 coins")
        } else {
            $.ajax({
                url: '/api/game',
                type: 'POST',
                data: {
                    'player': $("#player-name").text(),
                    'bet': bet
                },
                dataType: 'json',
                success: function(data) {
                    sessionStorage.setItem('game_id', data.id)
                    initial_pull();
                },
                error: function(e) {
                    alert('Internal server error!')
                }
            });
        }
    });
    function disable_bet() {
        more.attr('disabled', 'disabled');
        less.attr('disabled', 'disabled');
        deal.css({'display': 'none'});
        game_buttons.css({'display': 'inline-block'});
    }
    function enable_bet() {
        more.attr('disabled', 'inline-block');
        less.attr('disabled', 'inline-block');
    }
    function take_card(to_dealer, card_place, total_class, is_new_card, more=0, is_initial=false) {
        $.ajax({
            url: '/api/card',
            type: 'POST',
            data: {
                'gameId': sessionStorage.getItem('game_id'),
                'toDealer': to_dealer
            },
            dataType: 'json',
            success: function(card) {
                $(card_place).addClass(fromValue(card.value) + "-of-" + card.type + "s").removeClass("flipped");
                setTotalIn(total_class, to_dealer, is_new_card, false, more, is_initial)
            },
            error: function(e) {
                alert('Internal server error!')
            }
        });
    }
    function setTotalIn(total_class, to_dealer, is_new_card, from_double, more=0, is_initial=false) {
        $.ajax({
            url: '/api/total',
            type: 'GET',
            data: {
                'gameId': sessionStorage.getItem('game_id'),
                'toDealer': to_dealer
            },
            dataType: 'json',
            success: function(data) {
                $(total_class).text(data.total)
                if (more > 0) {
                    if (more == 2) {
                        sleep(400).then(() => {
                            take_card('False', ".player-cards .card2", ".player-total", false, 1);
                        });
                    } else if (more == 1) {
                        sleep(400).then(() => {
                            take_card('True', ".dealer-cards .card1", ".dealer-total", false, 0);
                        });
                    }
                } else {
                    if (is_initial) {
                        let playerTotal = parseInt(player_total.text());
                        if (playerTotal >= 9 && playerTotal <= 11) {
                            double.removeAttr('disabled');
                        }
                    }
                    if (to_dealer == 'True' && is_new_card &&
                        parseInt(dealer_total.text()) < 17) {
                        sleep(500).then(() => {
                            take_new_card('True', ".dealer-cards", ".dealer-total", false);
                        });
                    } else if (to_dealer == 'True' && is_new_card &&
                        parseInt(dealer_total.text()) >= 17) {
                        checkWinner();
                    } else if (parseInt(player_total.text()) > 21) {
                        lost();
                    } else if (from_double) {
                        if (parseInt(player_total.text()) > 21) {
                            lost();
                        }
                        sleep(500).then(() => {
                            stand.trigger("click");
                        });
                    }  
                } 
            },
            error: function(e) {
                alert('Internal server error!')
            }
        });
    }
    function initial_pull() {
        disable_bet();
        take_card('False', ".player-cards .card1", ".player-total", false, 2, is_initial=true);
    }
    async function playDealer() {
        take_card('True', ".dealer-cards .card2", ".dealer-total", true);
    }
    function fromValue(value) {
        switch (value) {
            case '2':
                return 'two';
            case '3':
                return 'three';
            case '4':
                return 'four';
            case '5':
                return 'five';
            case '6':
                return 'six';
            case '7':
                return 'seven';
            case '8':
                return 'eight';
            case '9':
                return 'nine';
            case '10':
                return 'ten';
            case 'J':
                return 'jack';
            case 'Q':
                return 'queen';
            case 'K':
                return 'king';
            case 'A':
                return 'ace';
        }
    }
});