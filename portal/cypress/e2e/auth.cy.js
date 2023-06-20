describe('template spec', () => {
  it('Visit front-end website', () => {
    cy.visit('http://127.0.0.1:8080')
    
    cy.contains('Login').click()
    cy.url().should('include', '/login')
  
    cy.get('input[type="username"]').type('notanuser@email.com')
    cy.get('input[type="password"]').type('password')
    
    cy.get('button[type="submit"]').click()
    
    //credentials are wrong, so it should stay on the same page
    //cy.getCookie('access-token-cookie').should('exist')
    
    cy.url().should('include', '/login')
    cy.on('window:alert', (str) => {
      expect(str).to.equal('Credenciales inválidas')
    })
    
    cy.login('pepe@mujica.com', '123')
    
    })
})