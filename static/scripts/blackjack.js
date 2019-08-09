$(document).ready(function(){

    // Patikrinti sessionTokeno game_id, ar jis egzistuoja. TAIP -> ziureti statusa ir jei ingame, tai grazinti zaidima, jei ne -> is naujo ikrauna zaidima


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
    $("#more").click(function() {
        let fund = parseInt($("#money").text());
        if (fund >= 10) {
            $("#money").text(fund - 10);
            let bet = parseInt($("#bet").text())
            $("#bet").text(bet + 10);
        } else {
            alert('You need to have at least 10 coins');
        }
    }),
    $("#less").click(function() {
        let bet = parseInt($("#bet").text());
        let minus = 10;
        if (bet >= 0 && bet < minus)
            minus = bet;
        $("#bet").text(bet - minus);
        let fund = parseInt($("#money").text())
        $("#money").text(fund + minus);
    });
    $("#hit").click(function() {
        let response = {
            'gameUid': '111',
            'userType': 'player',
            'card': {
                'type': 'diamond',
                'value': '10'
            },
            'totalSum': '24'
        };
        let card = response.card;
        let className = fromValue(card.value) + "-of-" + card.type + "s";
        $(".player-cards .new-cards").append("<div class='card two-of-hearts'></div>");
        let width = parseInt($(".player-cards").css("width"));
        $(".player-cards").css({"width": (width + 84).toString()})
        $(".player-total").text(response.totalSum);

        if (parseInt(response.totalSum) > 21) {
            if ($(".player-cards2").length) {
                $(".player-cards2").after($(".buttons"));
                alert('123')
            } else {
                lost();
            }
        }
    });
    function setGameResult(resultMessage) {
        $("#game-result").text(resultMessage);
    }
    function won() {
        $("#hit").attr('disabled', 'disabled');
        $("#stand").attr('disabled', 'disabled');

        $("#game-result").text('You won!');
        $(".game-finish").css({'display': 'inline-block'});

        $("#money").text(parseInt($("#money").text()) + parseInt($("#bet").text()));
    }
    function lost() {
        $("#hit").attr('disabled', 'disabled');
        $("#stand").attr('disabled', 'disabled');

        $("#game-result").text('You lost!');
        $(".game-finish").css({'display': 'inline-block'});

        $("#bet").text("0");
    }
    function draw() {
        $("#hit").attr('disabled', 'disabled');
        $("#stand").attr('disabled', 'disabled');

        $("#game-result").text('Draw!');
        $(".game-finish").css({'display': 'inline-block'});
    }
    $("#stand").click(function() {
        $("#hit").attr('disabled', 'disabled');
        $("#stand").attr('disabled', 'disabled');

        playDealer();
        checkWinner();
    });
    function checkWinner() {
        let dealerTotal = parseInt($("#dealerTotal").text());
        let playerTotal = parseInt($("#playerTotal").text());
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
        $(".game-finish").css({'display': 'none'});
        $(".game-buttons").css({'display': 'none'});
        $("#hit").removeAttr('disabled');
        $("#stand").removeAttr('disabled');
        $("#less").removeAttr('disabled');
        $("#more").removeAttr('disabled');
        $("#deal").css({'display': 'inline-block'});

        $(".new-cards").empty();
        $(".player-cards .card1").addClass("flipped");
        $(".player-cards .card2").addClass("flipped");
        $(".dealer-cards .card1").addClass("flipped");
        $(".dealer-cards .card2").addClass("flipped");
        $(".player-cards").css({"width": (164).toString()})
        $(".dealer-cards").css({"width": (164).toString()})

        $(".player-total").text("0");
        $(".dealer-total").text("0");
    });
    // $("#split").click(function() {
    //     $("#double").attr('disabled', 'disabled'), $("#split").attr('disabled', 'disabled');

    //     $(".player-cards").after("<div class='player-cards2'></div>");
    //     $(".player-cards2").append($(".player-cards .card2"));
    //     $(".player-cards .card2").css({'margin-left': '0px'});
    //     $(".player-cards .card2").css({'margin-top': '5px'});
    //     $(".player-cards").after($(".buttons"));
    //     $(".buttons").css({"width": (940).toString()})
    //     $(".player-cards2").after("<div class='clear' style='margin-bottom: 20px;'></div>");

    //     $(".player-cards").css({"width": (80).toString()})
    // });
    $("#double").click(function() {
        let bet = parseInt($("#bet").text());
        let fund = parseInt($("#money").text());
        if (bet > fund) {
            alert('You have not enough money!');
        } else {
            $("#bet").text(2 * bet);
            $("#money").text(fund - bet);
            $("#double").attr('disabled', 'disabled');
            $("#hit").attr('disabled', 'disabled');
            $("#stand").attr('disabled', 'disabled');
            $("#split").attr('disabled', 'disabled');

            let response = {
                'gameUid': '111',
                'userType': 'player',
                'card': {
                    'type': 'diamond',
                    'value': '10'
                },
                'totalSum': '20'
            };
            let card = response.card;
            let className = fromValue(card.value) + "-of-" + card.type + "s";
            $(".player-cards .new-cards").append("<div class='card two-of-hearts'></div>");
            let width = parseInt($(".player-cards").css("width"));
            $(".player-cards").css({"width": (width + 84).toString()})
            $(".player-total").text(response.totalSum);

            if (parseInt(response.totalSum) > 21) {
                lost();
            }
            sleep(500).then(() => {
                $("#stand").trigger("click");
            });
       
        }
    });
    function sleep (time) {
        return new Promise((resolve) => setTimeout(resolve, time));
      }
    $("#deal").click(function() {
        let bet = parseInt($("#bet").text());
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
        $("#more").attr('disabled', 'disabled');
        $("#less").attr('disabled', 'disabled');
        $("#deal").css({'display': 'none'});
        $(".game-buttons").css({'display': 'inline-block'});
    }
    function enable_bet() {
        $("#more").attr('disabled', 'inline-block');
        $("#less").attr('disabled', 'inline-block');
    }
    function take_card(direction, card_place, total_place) {
        $.ajax({
            url: '/api/card',
            type: 'POST',
            data: {
                'gameId': sessionStorage.getItem('game_id'),
                'toDealer': direction
            },
            dataType: 'json',
            success: function(card) {
                setClassIn({'type': card.type, 'value': card.value}, card_place);
                // gauti visu kordu reiksmes
                $(total_place).text(10);
            },
            error: function(e) {
                alert('Internal server error!')
            }
        });
    }
    function initial_pull() {
        disable_bet();
        take_card('False', ".player-cards .card1", ".player-total");
        sleep(400).then(() => {
            take_card('False', ".player-cards .card2", ".player-total");
            sleep(400).then(() => {
                take_card('True', ".dealer-cards .card1", ".dealer-total");
            });
        });
        let playerTotal = parseInt($(".player-total").text());
        if (playerTotal >= 9 && playerTotal <= 11) {
            $("#double").removeAttr('disabled');
        }
        if (response1.card.value == response3.card.value) {
            $("#split").removeAttr('disabled');
        }
    }
    function playDealer() {
        response = {
            'gameUid': '111',
            'userType': 'dealer',
            'card': {
                'type': 'heart',
                'value': '7'
            },
            'totalSum': '14'
        }

        setClassIn(response.card, ".dealer-cards .card2");
        $(".dealer-total").text(response.totalSum);

        var dealerTotal = parseInt($(".dealer-total").text());
        while(dealerTotal < 17) {
            let response = {
                'gameUid': '111',
                    'userType': 'dealer',
                    'card': {
                        'type': 'spade',
                        'value': '10'
                    },
                    'totalSum': '24'
            };

            let card = response.card;
            let className = fromValue(card.value) + "-of-" + card.type + "s";
            $(".dealer-cards .new-cards").append("<div class='card two-of-hearts'></div>");
            let width = parseInt($(".dealer-cards").css("width"));
            $(".dealer-cards").css({"width": (width + 84).toString()})
            $(".dealer-total").text(response.totalSum);
            // setClassIn(response.card, ".dealer-cards .card1");
            // $(".dealer-total").text(response.totalSum);
            dealerTotal = parseInt($(".dealer-total").text());
        }

        setClassIn(response.card, ".dealer-cards .card2");
        // play while gives 17 or above
    }

    function setClassIn(card, placeIn) {
        $(placeIn).addClass(fromValue(card.value) + "-of-" + card.type + "s");
        $(placeIn).removeClass("flipped");
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