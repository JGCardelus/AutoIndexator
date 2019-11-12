function mounted() {
    window.addEventListener("keydown", function(e) {
        if (e.keyCode == 9)
        {
            e.preventDefault();
        }
        console.log(e.code);
    });
}

mounted();

let searched_terms = [];
function search(a)
{
    data = a.value;
    if (data.length == 0)
    {
        searched_terms = [];
    }
    else
    {
        if (searched_terms.length == 0)
        {
            eel.start_search(data);
            searched_terms.push(data)
        }
        else
        {
            eel.search(data)
            searched_terms.push(data)
        }
    }  
}