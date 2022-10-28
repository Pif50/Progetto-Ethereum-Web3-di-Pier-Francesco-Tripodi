//colours to assiged(depending on random number)
function getHouses(typeHouses = 0) {
  return (
    ["GRYFFINDOR", "HUFFLEPUFF", "RAVENCLAW", "SLYTHERIN"][typeHouses] ||
    "GRYFFINDOR"
  );
}

//var with random generated
export function getRaffle() {
  return getHouses(Math.floor(Math.random() * 4));
}
