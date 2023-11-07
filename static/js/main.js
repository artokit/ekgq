document.body.addEventListener("mousemove", (e) => {
	let maxDegX = 7;
	let maxDegY = 5;

	let clientMouseX = e.pageX;
	let clientMouseY = e.pageY;

	let windowSizeX = window.innerWidth;
	let windowSizeY = window.innerHeight;
	
	let rotateY = -(maxDegX*(clientMouseX/windowSizeX) - maxDegX/2);
	let rotateX = maxDegY*(clientMouseY/windowSizeY) - maxDegY/2;

	document.querySelector('.mainMenu').style.transform = `rotateY(${rotateY}deg) rotateX(${rotateX}deg)`;
	
	for (let elem of document.querySelectorAll('.paralaxElem')) {
		let rect = elem.getBoundingClientRect();
		let rY = 1 - (clientMouseX/(rect.x + rect.width/2));
		let rX = 1 - (clientMouseY/(rect.y + rect.height/2));
		elem.style.transform = `rotateY(${-rY*40}deg) rotateX(${Math.max(rX, -1)*20}deg)`;
	}
});
