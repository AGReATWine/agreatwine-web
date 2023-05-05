const sortBtns = document.querySelectorAll(".sort-btn");
let sortOrder = "desc"; // initialize sort order to descending

sortBtns.forEach(sortBtn => {
  sortBtn.addEventListener("click", () => {
    
    const sortingGroup = sortBtn.parentElement.nextElementSibling;
    const sortingElement = sortBtn.parentElement.nextElementSibling.querySelectorAll(".sorting-element");
    const sortingElementArray = Array.from(sortingElement);
    console.log(sortingElementArray)
  
    if (sortOrder === "desc") {    
      sortingElementArray.sort((a, b) => {
        const aValue = parseInt(b.querySelector(".sort-value").style.width);
        const bValue = parseInt(a.querySelector(".sort-value").style.width);
        return aValue - bValue;
      });
      sortOrder = "asc";
      sortBtn.classList.replace("bi-sort-down", "bi-sort-up");
    } else {
      sortingElementArray.sort((a, b) => {
        const aValue = parseInt(a.querySelector(".sort-value").style.width);       const bValue = parseInt(b.querySelector(".sort-value").style.width);
        return aValue - bValue;
      });
      sortOrder = "desc";
      sortBtn.classList.replace("bi-sort-up", "bi-sort-down");
    }
  
    sortingElement.innerHTML = "";
    sortingElementArray.forEach((item) => {
      sortingGroup.appendChild(item);
    });
  });
});

document.addEventListener('DOMContentLoaded', function() {
  var filterInput = document.querySelector('#filterInput');
  
  if (filterInput) {
    filterInput.addEventListener('input', function() {
      var filterValue = this.value.toLowerCase().trim();
      var elements = document.querySelectorAll('[data-name]');

      for (var i = 0; i < elements.length; i++) {
          var element = elements[i];
          var name = element.getAttribute('data-name').toLowerCase();

          if (name.indexOf(filterValue) === -1) {
              element.classList.add('d-none');
          } else {
              element.classList.remove('d-none');
          }
      }
    });
  }
});

const filterInput = document.querySelector('#filter-input');
const entries = Array.from(document.querySelectorAll('.sorting-element'));

if (filterInput) {
  filterInput.addEventListener('keyup', () => {
    const filterValue = filterInput.value.toLowerCase().trim();

    entries.forEach(entry => {
      const title = entry.querySelector('.text-danger');
      const subtitle = entry.querySelector('.mb-1:not(.text-danger)');
      const text = [title, subtitle].filter(el => el !== null).map(el => el.textContent.toLowerCase().trim()).join(' ');

      if (filterValue === '' || text.includes(filterValue)) {
        entry.style.display = '';
      } else {
        entry.style.display = 'none';
      }
    });
  });
}

///////////////////////////////////////////////////////
