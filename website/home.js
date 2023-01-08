// Velo API Reference: https://www.wix.com/velo/reference/api-overview/introduction
import {session} from 'wix-storage';
import wixLocation from 'wix-location'

$w.onReady(function () {
    

    // Write your Javascript code here using the Velo framework API

    // Print hello world:
    // console.log("Hello world!");

    // Call functions on page elements, e.g.:
    // $w("#button1").label = "Click me!";

    // Click "Run", or Preview your site, to execute your code
    session.setItem("globalClick",0);
    countdownTimer();

});

async function countdownTimer() {
    let date = await new Date('2023-03-01T12:30:00').getTime();

    let downTime = setInterval(function () {
        let nowTime = new Date().getTime();
        let diff = date - nowTime;
        let seconds = Math.floor((((diff % (1000 * 60)) / 1000) % 16));

        $w("#seconds").text = seconds.toString();
        if($w("#seconds").text == "0"){
            console.log("This works")
            wixLocation.to("/scrresultpage");
        }
    }, 1000)
}

/**
*	Adds an event handler that runs when the element is clicked.
	[Read more](https://www.wix.com/corvid/reference/$w.ClickableMixin.html#onClick)
*	 @param {$w.MouseEvent} event
*/
export function section1_click(event) {
    // This function was added from the Properties & Events panel. To learn more, visit http://wix.to/UcBnC-4
    // Add your code for this event here:

}



/**
*	Adds an event handler that runs when the element is clicked.
	[Read more](https://www.wix.com/corvid/reference/$w.ClickableMixin.html#onClick)
*	 @param {$w.MouseEvent} event
*/
export function ButtonA_click(event) {
	// This function was added from the Properties & Events panel. To learn more, visit http://wix.to/UcBnC-4
	// Add your code for this event here: 
    session.setItem("choice","A")
}

/**
*	Adds an event handler that runs when the element is clicked.
	[Read more](https://www.wix.com/corvid/reference/$w.ClickableMixin.html#onClick)
*	 @param {$w.MouseEvent} event
*/
export function mobileButton1_click(event) {
	// This function was added from the Properties & Events panel. To learn more, visit http://wix.to/UcBnC-4
	// Add your code for this event here: 
}

/**
*	Adds an event handler that runs when the element is clicked.
	[Read more](https://www.wix.com/corvid/reference/$w.ClickableMixin.html#onClick)
*	 @param {$w.MouseEvent} event
*/
export function buttonB_click(event) {
	// This function was added from the Properties & Events panel. To learn more, visit http://wix.to/UcBnC-4
	// Add your code for this event here: 
    session.setItem("choice","B")
}

/**
*	Adds an event handler that runs when the element is clicked.
	[Read more](https://www.wix.com/corvid/reference/$w.ClickableMixin.html#onClick)
*	 @param {$w.MouseEvent} event
*/
export function addClick_click(event) {
	// This function was added from the Properties & Events panel. To learn more, visit http://wix.to/UcBnC-4
	// Add your code for this event here: 
    session.setItem("globalClick", parseInt(session.getItem("globalClick")) + 1);
     let downTime = setInterval(function () {
        $w("#clicks").text = session.getItem("globalClick").toString();
        }
    , 1000);
}