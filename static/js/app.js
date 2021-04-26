//alert(board_python_to_js['board']);



const player = "0";
const computer = "X";

let board_full = false;
let play_board = ["", "", "", "", "", "", "", "", ""];
play_board = board_python_to_js['board']; // python to js



const board_container = document.querySelector(".play-area");

const winner_statement = document.getElementById("winner");

check_board_complete = () => {
  let flag = true;
  play_board.forEach(element => {
    if (element != player && element != computer) {
      flag = false;
    }
  });
  board_full = flag;
};

const check_line = (a, b, c) => {
  return (
    play_board[a] == play_board[b] &&
    play_board[b] == play_board[c] &&
    (play_board[a] == player || play_board[a] == computer)
  );
};

const check_match = () => {
  for (i = 0; i < 9; i += 3) {
    if (check_line(i, i + 1, i + 2)) {
      return play_board[i];
    }
  }
  for (i = 0; i < 3; i++) {
    if (check_line(i, i + 3, i + 6)) {
      return play_board[i];
    }
  }
  if (check_line(0, 4, 8)) {
    return play_board[0];
  }
  if (check_line(2, 4, 6)) {
    return play_board[2];
  }
  return "";
};

const check_for_winner = () => {
  let res = check_match()
  if (res == player) {
    winner.innerText = "Winner is player!!";
    winner.classList.add("playerWin");
    board_full = true
  } else if (res == computer) {
    winner.innerText = "Winner is computer";
    winner.classList.add("computerWin");
    board_full = true
  } else if (board_full) {
    winner.innerText = "Draw!";
    winner.classList.add("draw");
  }
};


const render_board = () => {
  board_container.innerHTML = ""
  play_board.forEach((e, i) => {
    board_container.innerHTML += `<div id="block_${i}" class="block" onclick="{{addPlayerMove(${i})}}">${play_board[i]}</div> `
    if (e == player || e == computer) {
      document.querySelector(`#block_${i}`).classList.add("occupied");
    }
  });

  //console.log(play_board)

};


const callApi = () => {
  // Meu Método Post para pegar a Variável do JS e enviar para o FLASK
  $.ajax({
    type: 'POST',
    url: '/',
    data: JSON.stringify ( {'board' : play_board } ),
    contentType: "application/json",
    dataType: 'json'
  })
  .done(function(msg){
    console.log(msg)
    addComputerMove(msg)
  })
  .fail(function(jqXHR, textStatus, msg){
    console.log( jqXHR, textStatus, msg )
  });
};




const game_loop = () => {
  render_board();
  check_board_complete();
  check_for_winner();
}

const addPlayerMove = e => {
  if (!board_full && play_board[e] == "") {
    play_board[e] = player;
    //console.log( play_board);
    game_loop();
    callApi();
    //addComputerMove();
  }
};

const addComputerMove = (a) => {
  //if (!board_full) {
  //  do {
  //    selected = Math.floor(Math.random() * 9);
  //  } while (play_board[selected] != "");
  // play_board[selected] = computer;
    //console.log( a, ' .....chamou....')
    play_board = a;
    game_loop();
  //}
};

const reset_board = () => {
  play_board = ["", "", "", "", "", "", "", "", ""];
  board_full = false;
  winner.classList.remove("playerWin");
  winner.classList.remove("computerWin");
  winner.classList.remove("draw");
  winner.innerText = "";

  $.ajax({
    type: 'POST',
    url: '/reset',
    data: JSON.stringify ( {'board' : play_board } ),
    contentType: "application/json",
    dataType: 'json'
  })
  .done(function(msg){
    console.log(msg);
    addComputerMove(msg);
    render_board();
  })
  .fail(function(jqXHR, textStatus, msg){
    console.log( jqXHR, textStatus, msg )
  });

  


};

//initial render
render_board();

