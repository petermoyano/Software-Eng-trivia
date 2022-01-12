const allFlashes = document.getElementsByClassName('alert')

$('p select').addClass("form-select text-center m-3 p-2 text-warning bg-dark");
$('form p label').addClass("col-12 col-form-label text-center my-4 p-2 text-warning");
$('form p input').addClass("col-8 form-control text-center bg-dark");


/* btnForFlashes adds the necesary html markup to make the flashes dynamically generated in the back end,
 responsive and dismissible *****************************************************************************/
function btnForflashes(allFlashes) {
    for (let flash of allFlashes) {
        let pyhtonClass = flash.getAttribute("class");
        flash.setAttribute("class", `${pyhtonClass} alert-dismissible fade show text-center my-3`);
        flash.insertAdjacentHTML('beforeend', '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>')
    }
}
btnForflashes(allFlashes);

/* The following 4 lines are for the Bootstrap trigger to enable flash removal **/
const alertList = document.querySelectorAll('.alert')
alertList.forEach(function (alert) {
    new bootstrap.Alert(alert)
})
/* *********************************************************************************************** */
