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

const getFilterFaq = document.getElementById('getFilterFaq');
if (getFilterFaq) {
  getFilterFaq.addEventListener('input', filterFaq);

  function filterFaq() {
    var filterValue = getFilterFaq.value.toLowerCase();
    var accordionItems = document.getElementsByClassName('accordion-item');

    for (var i = 0; i < accordionItems.length; i++) {
      var accordionButton = accordionItems[i].querySelector('.accordion-button');
      var accordionBody = accordionItems[i].querySelector('.accordion-body');

      var buttonText = accordionButton.textContent;
      var bodyText = accordionBody.textContent;

      if (filterValue === '') {
        // If filterValue is empty, remove the highlighting
        accordionButton.innerHTML = buttonText;
        accordionBody.innerHTML = bodyText;
        accordionItems[i].style.display = '';
      } else if (
        buttonText.toLowerCase().includes(filterValue) ||
        bodyText.toLowerCase().includes(filterValue)
      ) {
        // Highlight matched string in button text
        accordionButton.innerHTML = highlightMatchedString(buttonText, filterValue);

        // Highlight matched string in body text
        accordionBody.innerHTML = highlightMatchedString(bodyText, filterValue);

        accordionItems[i].style.display = '';
      } else {
        accordionItems[i].style.display = 'none';
      }
    }
  }

  function highlightMatchedString(text, filterValue) {
    // Regex pattern to match the filterValue case-insensitively
    var regex = new RegExp(`(${filterValue})`, 'gi');

    // Wrap matched string in <mark> tags to highlight it
    var highlightedText = text.replace(regex, '<mark>$1</mark>');

    return highlightedText;
  }
}




///////////////////////////////////////////////////////
