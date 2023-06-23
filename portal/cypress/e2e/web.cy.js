describe('Test Web functionality', () => {


  beforeEach(() => {
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
  });


  it('Obtain Disciplines for member logged', () => {
    cy.contains('Disciplinas').click()
  })

  it('Obtain Statistics for member logged', () => {
    cy.contains('Estadisticas').click()
  })

  it('Obtain Payments for member logged', () => {
    cy.contains('Mis Pagos').click()
  })
})