describe('Test APIs without login', () => {


  // ----------------------------------------
  // API para obtener la Informacion del Club
  // ----------------------------------------
  it('API Club test Info', () => { 
    cy.request({
      method: 'GET',
      url: 'http://localhost:5001/api/club/info',
      headers:{
              'Content-Type':'application/json'
              }      

    }).then( (response) => {
      expect(response.status).to.equal(200)
      expect(response.body.email).to.equal('clubdeportivovillaelisa@gmail.com')
      expect(response.body.phone).to.equal('0221 487-0193')
    })
  })



  // ----------------------------------------
  // API para obtener todas las disciplinas
  // ----------------------------------------
  it('API Club test Disciplines', () => {  
    cy.request({
        method: 'GET',
        url: 'http://localhost:5001/api/club/disciplines',
        headers:{
                'Content-Type':'application/json'
                }      

    }).then( (response) => {
      expect(response.status).to.equal(200)
      expect(response.body[0].active).to.equal(true)
      expect(response.body[0].category).to.equal('Armas')
      expect(response.body[1].category).to.equal('Atletismo')
    })
  })


   // ----------------------------------------
  // API para obtener todas las disciplinas
  // ----------------------------------------
  it('API Members test Members', () => {  
    cy.request({
        method: 'GET',
        url: 'http://localhost:5001/api/members',
        headers:{
                'Content-Type':'application/json'
                }      

    }).then( (response) => {
      expect(response.status).to.equal(200)
      expect(response.body[0].first_name).to.equal('Nicolas')
      expect(response.body[0].last_name).to.equal('Barone')
    })
  })


})