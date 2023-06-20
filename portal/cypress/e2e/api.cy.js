describe('Test APIs', () => {

  beforeEach(() => {
    
    // --------------------------
    // API para realizar el login
    // --------------------------
    cy.request({
      method: 'POST',
      url: 'http://localhost:5001/api/auth/login',
      headers:{
              'Content-Type':'application/json'
              },
      body:{
        username:"nicolasbarone@gmail.com",
        password: "123"
      }        
    }).then( (response) => {
      expect(response.status).to.equal(200)
      expect(response.body.msg).to.equal("login succesful")
    })

  });



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


  // ----------------------------------------------------
  // API para obtener todas las disciplinas de un miembro
  // ---------------------------------------------------- 
  it('API Club test Disciplines by Member', () => {  
    cy.request({
        method: 'GET',
        url: 'http://localhost:5001/api/club/disciplines',
        headers:{
                'Content-Type':'application/json',
                'Authorization': 1
                }
    }).then( (response) => {
      expect(response.status).to.equal(200)
      expect(response.body[0].active).to.equal(true)
      expect(response.body[0].category).to.equal('Armas')
    })
  })



  // ----------------------------------------
  // API para obtener el Perfil de un miembro
  // ----------------------------------------
  it('API Me test Profile of some member', () => {
    cy.request({
      method: 'GET',
      url: 'http://localhost:5001/api/me/profile',
      headers:{
              'Content-Type':'application/json',
              'Authorization': 1
              }
    }).then( (response) => {
      expect(response.status).to.equal(200)
      expect(response.body.first_name).to.equal('Nicolas')
      expect(response.body.last_name).to.equal('Barone')
    })

  })


})