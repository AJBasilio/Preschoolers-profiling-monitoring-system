$(document).ready(function() {
    activeLink()
    change_label()
    
    
    
})

function activeLink() {
    $('.navbar-nav .nav-item a').click(function() {

        $('.nav-link').removeClass('active')
        

        $(this).closest('.nav-link').addClass('active')
    })
}

function change_label(){
    var selected = document.getElementById('type').value;

    if (String(selected) == "Admission") {
        document.getElementById('user-lbl').innerHTML = "Admission ID:";
    }
    else if (String(selected) == "Applicant") {
        document.getElementById('user-lbl').innerHTML = "Reference Number:";
    }
    else if (String(selected) == "Nurse") {
        document.getElementById('user-lbl').innerHTML = "Nurse ID:";
    }
    else if (String(selected) == "Interviewer") {
        document.getElementById('user-lbl').innerHTML = "Interviewer ID:";
    }
    console.log(selected);
}

