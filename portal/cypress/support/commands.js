// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })

Cypress.Commands.add('login', (username, password) => {
    cy.session(
      username,
      () => {
        cy.visit('http://127.0.0.1:8080')
        cy.contains('Login').click()
        cy.url().should('include', '/login')
        cy.get('input[type=username]').type(username)
        cy.get('input[type=password]').type(`${password}{enter}`, { log: false })
        cy.getCookie('access_token_cookie').should('exist')
        
      },
      {
        validate: () => {
          cy.getCookie('access_token_cookie').should('exist')
        },
      }
    )
  })