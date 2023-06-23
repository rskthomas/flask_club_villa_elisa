describe('Test Login', () => {

  it('Visit front-end website and Wrong Login', () => {
    Cypress.on('uncaught:exception', (err, runnable) => {
      return false
    })
  
    cy.visit('http://localhost:3000')
    
    // Hace click en el link Login
    cy.contains('Login').click()
    cy.url().should('include', '/login')
  
    // Ingresamos los datos para Loguearnos y realiza el Logueo
    cy.get('input[type="username"]').type('notanuser@email.com')
    cy.get('input[type="password"]').type('password')

    cy.get('button[type="submit"]').click();
    
    // Realiza algunas validaciones
    cy.url().should('include', '/login')
    cy.on('window:alert', (str) => {
      expect(str).to.equal('Credenciales inválidas')
    })
  })


  it('Visit front-end website and Login OK', () => {
    Cypress.on('uncaught:exception', (err, runnable) => {
      return false
    })
  
    cy.visit('http://localhost:3000')
    
    // Hace click en el link Login
    cy.contains('Login').click()
    cy.url().should('include', '/login')
  
    // Ingresamos los datos para Loguearnos y realizar el Logueo
    cy.get('input[type="username"]').type('nicolasbarone@gmail.com')
    cy.get('input[type="password"]').type('123')

    cy.get('button[type="submit"]').click();
    
    // Realiza algunas validaciones
    cy.contains('Logout')
  })


})